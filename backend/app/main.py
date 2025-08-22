from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from pydantic import BaseModel
from schemas import GameCreateRequest, GameResponse, PlayerJoinRequest, PlayerResponse, AnswerRequest, AnswerResponse
from models import Game, User, Question as QuestionModel, QuestionOption as QuestionOptionModel
from datetime import datetime
import random, string

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"status": "healthy",
            "Code": 200,
            "Message": "Service is running smoothly."}

def generate_unique_join_code(db: Session, length=6):
    while True:
        join_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        # Check if this code already exists
        existing_game = db.query(Game).filter(Game.join_code == join_code).first()
        if not existing_game:
            return join_code
        
def get_or_create_host(db: Session, host_id: str = None):
    """Get existing user or create anonymous host"""
    if host_id:
        # Try to find existing user
        user = db.query(User).filter(User.id == host_id).first()
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="Host user not found")
    else:
        # Create anonymous host
        new_user = User(
            username=None,  # Anonymous
            email=None,
            is_host=True,
            created_at=datetime.utcnow()
        )
        db.add(new_user)
        db.flush()  # Get the ID without committing
        return new_user

def generate_sample_questions(prompt: str):
    # Temp function will be replaced with Gemini API call
    sample_questions = [
        {
            "question_text": f"Sample question about {prompt}?",
            "question_type": "MCQ",
            "source_type": "prompt",
            "points_value": 10,
            "explanation": "This is a sample explanation",
            "time_limit": 30,
            "options": [
                {"option_text": "Option A", "option_order": 1, "is_correct": True},   # Mark one as correct
                {"option_text": "Option B", "option_order": 2, "is_correct": False},
                {"option_text": "Option C", "option_order": 3, "is_correct": False},
                {"option_text": "Option D", "option_order": 4, "is_correct": False}
            ]
        },
        {
            "question_text": f"True or False: {prompt} is interesting?",
            "question_type": "TF",
            "source_type": "prompt", 
            "points_value": 5,
            "explanation": "This is subjective",
            "time_limit": 15,
            "options": [
                {"option_text": "True", "option_order": 1, "is_correct": True},
                {"option_text": "False", "option_order": 2, "is_correct": False}
            ]
        }
    ]
    return sample_questions

@app.post("/game/create", response_model=GameResponse)
def create_game(game: GameCreateRequest, db: Session = Depends(get_db)):
    try:
        # Step 1: Handle host user
        host_user = get_or_create_host(db, game.host_id)
        
        # Step 2: Generate unique join code
        join_code = generate_unique_join_code(db)
        
        # Step 3: Create game record
        new_game = Game(
            topic=game.prompt,
            host_user_id=host_user.id,
            start_time=datetime.utcnow(),
            duration=600,  # 10 minutes default
            status="pending",
            join_code=join_code
        )
        db.add(new_game)
        db.flush()  # Get the game ID
        
        # Step 4: Generate questions (stub for now)
        questions_data = generate_sample_questions(game.prompt)
        
        # Step 5: Save questions and options to database
        created_questions = []
        for q_data in questions_data:
            # Create question
            question = QuestionModel(
                game_id=new_game.id,
                question_text=q_data["question_text"],
                question_type=q_data["question_type"],
                source_type=q_data["source_type"],
                points_value=q_data["points_value"],
                explanation=q_data["explanation"],
                time_limit=q_data["time_limit"],
                is_active=True
            )
            db.add(question)
            db.flush()  # Get question ID
            
            # Create options for this question
            options = []
            for opt_data in q_data["options"]:
                option = QuestionOptionModel(
                    question_id=question.id,
                    option_text=opt_data["option_text"],
                    option_order=opt_data["option_order"],
                    is_correct=opt_data["is_correct"]
                )
                db.add(option)
                db.flush()  # Get the option ID
                options.append(option)
            
            # Add to response data
            created_questions.append({
                "id": str(question.id),
                "question_text": question.question_text,
                "question_type": question.question_type,
                "source_type": question.source_type,
                "points_value": question.points_value,
                "explanation": question.explanation,
                "time_limit": question.time_limit,
                "is_active": question.is_active,
                "options": [{
                    "id": str(opt.id),
                    "question_id": str(opt.question_id),
                    "option_text": opt.option_text,
                    "option_order": opt.option_order,
                    "is_correct": opt.is_correct
                } for opt in options]
            })
        
        # Step 6: Commit all changes
        db.commit()
        
        # Step 7: Return response
        return GameResponse(
            game_id=str(new_game.id),
            join_code=new_game.join_code,
            status="created",
            message="Game created successfully",
            questions=created_questions
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create game: {str(e)}")

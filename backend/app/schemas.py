''' Define Pydantic models for:
Game creation (GameCreateRequest)
Game response (GameResponse)
Player join (PlayerJoinRequest, PlayerResponse)
Answer submission (AnswerRequest, AnswerResponse)
Question/Option models as needed'''

from typing import Optional
from pydantic import BaseModel

class GameCreateRequest(BaseModel):
  prompt: str
  host_id: Optional[int] = None  # Optional host ID, defaults to None

class PlayerJoinRequest(BaseModel):
    game_id: str
    display_name: str

class PlayerResponse(BaseModel):
    player_id: str
    display_name: str
    joined_at: str

class AnswerRequest(BaseModel):
    player_id: str
    question_id: str
    answer_text: str

class AnswerResponse(BaseModel):
    success: bool
    message: str
    correct: bool
    correct_answer: str

class QuestionOption(BaseModel):
    id: str
    question_id: str
    option_text: str
    option_order: int
    is_correct: bool

class Question(BaseModel):
    id: str
    question_text: str
    question_type: str
    source_type: str
    points_value: int
    explanation: str
    time_limit: int
    is_active: bool
    options: list[QuestionOption] = []

class GameResponse(BaseModel):
  game_id: str
  join_code: str
  status: str
  message: str
  questions: list[Question] = []
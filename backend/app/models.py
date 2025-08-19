from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db import Base

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(200), nullable=False)
    host_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    duration = Column(Integer)
    status = Column(String(50))
    winner_name = Column(String(100))
    join_code = Column(String(10), unique=True, index=True)
    questions = relationship("Question", back_populates="game")
    players = relationship("Player", back_populates="game")
    host = relationship("User", back_populates="games")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    is_host = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)
    games = relationship("Game", back_populates="host")
    players = relationship("Player", back_populates="user")
  
class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    display_name = Column(String(100))
    score = Column(Integer, default=0)
    joined_at = Column(TIMESTAMP)
    game = relationship("Game", back_populates="players")
    user = relationship("User", back_populates="players")
    answers = relationship("Answer", back_populates="player")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    question_text = Column(Text, nullable=False)
    question_type = Column(String(10))
    source_type = Column(String(10))
    points_value = Column(Integer, default=1)
    explanation = Column(Text)
    time_limit = Column(Integer)
    is_active = Column(Boolean, default=True)
    game = relationship("Game", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question")
    answers = relationship("Answer", back_populates="question")

class QuestionOption(Base):
    __tablename__ = "question_options"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    option_text = Column(String(200))
    option_order = Column(Integer)
    question = relationship("Question", back_populates="options")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    selected_option_id = Column(Integer, ForeignKey("question_options.id"))
    is_correct = Column(Boolean)
    answered_at = Column(TIMESTAMP)
    player = relationship("Player", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    selected_option = relationship("QuestionOption")
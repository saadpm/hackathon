from sqlalchemy import Column, Integer, String, Text, JSON, Enum, DECIMAL, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
from models.skill import ProficiencyLevel


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    job_title_id = Column(Integer, ForeignKey("job_titles.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(255), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    correct_answer = Column(String(255), nullable=False)
    difficulty_level = Column(Enum(ProficiencyLevel), nullable=False, index=True)
    experience_level_years = Column(DECIMAL(3, 1))
    points = Column(Integer, default=1)
    explanation = Column(Text)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    job_title = relationship("JobTitle", back_populates="quiz_questions")
    creator = relationship("User", foreign_keys=[created_by])
    assessment_results = relationship("AssessmentResult", back_populates="quiz_question", cascade="all, delete-orphan")


class AssessmentResult(Base):
    __tablename__ = "assessment_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    quiz_question_id = Column(Integer, ForeignKey("quiz_questions.id", ondelete="CASCADE"), nullable=False)
    selected_answer = Column(String(255), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    points_earned = Column(Integer, default=0)
    time_taken_seconds = Column(Integer)
    attempted_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="assessment_results")
    quiz_question = relationship("QuizQuestion", back_populates="assessment_results")


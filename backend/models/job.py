from sqlalchemy import Column, Integer, String, Text, JSON, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base


class JobTitle(Base):
    __tablename__ = "job_titles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    level = Column(Integer, nullable=False, index=True)
    next_level_job_id = Column(Integer, ForeignKey("job_titles.id", ondelete="SET NULL"), nullable=True)
    department = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    next_level_job = relationship("JobTitle", remote_side=[id], backref="previous_level_jobs")
    job_descriptions = relationship("JobDescription", back_populates="job_title", cascade="all, delete-orphan")
    users = relationship("User", back_populates="job_title")
    quiz_questions = relationship("QuizQuestion", back_populates="job_title", cascade="all, delete-orphan")
    roadmaps = relationship("LearningRoadmap", back_populates="job_title", cascade="all, delete-orphan")


class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    job_title_id = Column(Integer, ForeignKey("job_titles.id", ondelete="CASCADE"), nullable=False, index=True)
    required_skills = Column(JSON, nullable=False)
    required_tools = Column(JSON, nullable=False)
    required_years_of_experience = Column(DECIMAL(3, 1), nullable=False)
    competency_weightage = Column(JSON)
    expected_proficiency_levels = Column(JSON)
    preferred_skills = Column(JSON)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    job_title = relationship("JobTitle", back_populates="job_descriptions")


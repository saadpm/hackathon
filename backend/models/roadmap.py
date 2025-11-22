from sqlalchemy import Column, Integer, String, Enum, JSON, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
from models.skill import ProficiencyLevel
import enum


class RoadmapStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"


class LearningRoadmap(Base):
    __tablename__ = "learning_roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    job_title_id = Column(Integer, ForeignKey("job_titles.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(255), nullable=False, index=True)
    current_level = Column(Enum(ProficiencyLevel))
    target_level = Column(Enum(ProficiencyLevel), nullable=False)
    gap_percentage = Column(DECIMAL(5, 2))
    milestones = Column(JSON, nullable=False)
    course_recommendations = Column(JSON)
    practice_tasks = Column(JSON)
    estimated_completion_weeks = Column(Integer)
    status = Column(Enum(RoadmapStatus), default=RoadmapStatus.NOT_STARTED)
    progress_percentage = Column(DECIMAL(5, 2), default=0)
    started_at = Column(TIMESTAMP, nullable=True)
    completed_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="roadmaps")
    job_title = relationship("JobTitle", back_populates="roadmaps")


from sqlalchemy import Column, Integer, String, Enum, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
import enum


class UserRole(str, enum.Enum):
    OD_MANAGER = "OD_MANAGER"
    EMPLOYEE = "EMPLOYEE"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.EMPLOYEE, index=True)
    job_title_id = Column(Integer, ForeignKey("job_titles.id", ondelete="SET NULL"), nullable=True)
    years_of_experience = Column(DECIMAL(3, 1), default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    job_title = relationship("JobTitle", back_populates="users")
    skills = relationship("EmployeeSkill", back_populates="user", cascade="all, delete-orphan")
    assessment_results = relationship("AssessmentResult", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("LearningRoadmap", back_populates="user", cascade="all, delete-orphan")


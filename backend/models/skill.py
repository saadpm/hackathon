from sqlalchemy import Column, Integer, String, Enum, DECIMAL, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
import enum


class ProficiencyLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class EmployeeSkill(Base):
    __tablename__ = "employee_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(255), nullable=False, index=True)
    proficiency_level = Column(Enum(ProficiencyLevel), nullable=False)
    years_of_experience = Column(DECIMAL(3, 1), default=0)
    self_assessment_score = Column(Integer)
    is_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="skills")


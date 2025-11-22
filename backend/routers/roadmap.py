from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
from middleware import get_current_user, get_current_employee
from models.user import User
from models.skill import EmployeeSkill
from models.roadmap import LearningRoadmap, RoadmapStatus
from models.job import JobDescription
from schemas import RoadmapGenerateRequest, LearningRoadmapResponse
from services import openai_service

router = APIRouter(prefix="/roadmap", tags=["Learning Roadmap"])


@router.post("/generate", response_model=LearningRoadmapResponse)
def generate_roadmap(
    request: RoadmapGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee)
):
    """
    Generate personalized learning roadmap for a skill
    """
    # Check if user has job title
    if not current_user.job_title_id:
        raise HTTPException(status_code=400, detail="No job title assigned")
    
    # Get job description
    jd = db.query(JobDescription).filter(
        JobDescription.job_title_id == current_user.job_title_id
    ).first()
    
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # Get current skill level
    current_skill = db.query(EmployeeSkill).filter(
        EmployeeSkill.user_id == current_user.id,
        EmployeeSkill.skill_name == request.skill_name
    ).first()
    
    current_level = current_skill.proficiency_level if current_skill else "beginner"
    
    # Calculate gap percentage
    proficiency_map = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}
    current_val = proficiency_map.get(current_level.value if hasattr(current_level, 'value') else current_level, 1)
    target_val = proficiency_map.get(request.target_level.value, 4)
    gap_percentage = ((target_val - current_val) / target_val) * 100 if target_val > current_val else 0
    
    # Generate roadmap using OpenAI
    roadmap_data = openai_service.generate_learning_roadmap(
        skill_name=request.skill_name,
        current_level=current_level.value if hasattr(current_level, 'value') else current_level,
        target_level=request.target_level.value,
        gap_percentage=gap_percentage,
        job_title=current_user.job_title.title
    )
    
    # Check if roadmap already exists
    existing_roadmap = db.query(LearningRoadmap).filter(
        LearningRoadmap.user_id == current_user.id,
        LearningRoadmap.skill_name == request.skill_name,
        LearningRoadmap.status != RoadmapStatus.COMPLETED
    ).first()
    
    if existing_roadmap:
        # Update existing roadmap
        existing_roadmap.target_level = request.target_level
        existing_roadmap.gap_percentage = gap_percentage
        existing_roadmap.milestones = roadmap_data.get("milestones", [])
        existing_roadmap.course_recommendations = roadmap_data.get("course_recommendations", [])
        existing_roadmap.practice_tasks = roadmap_data.get("practice_tasks", [])
        existing_roadmap.estimated_completion_weeks = roadmap_data.get("estimated_completion_weeks", 0)
        roadmap = existing_roadmap
    else:
        # Create new roadmap
        roadmap = LearningRoadmap(
            user_id=current_user.id,
            job_title_id=current_user.job_title_id,
            skill_name=request.skill_name,
            current_level=current_level,
            target_level=request.target_level,
            gap_percentage=gap_percentage,
            milestones=roadmap_data.get("milestones", []),
            course_recommendations=roadmap_data.get("course_recommendations", []),
            practice_tasks=roadmap_data.get("practice_tasks", []),
            estimated_completion_weeks=roadmap_data.get("estimated_completion_weeks", 0),
            status=RoadmapStatus.NOT_STARTED
        )
        db.add(roadmap)
    
    db.commit()
    db.refresh(roadmap)
    
    return roadmap


@router.get("/my-roadmaps", response_model=List[LearningRoadmapResponse])
def get_my_roadmaps(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee)
):
    """
    Get all roadmaps for current employee
    """
    roadmaps = db.query(LearningRoadmap).filter(
        LearningRoadmap.user_id == current_user.id
    ).all()
    
    return roadmaps


@router.put("/roadmaps/{roadmap_id}/progress")
def update_roadmap_progress(
    roadmap_id: int,
    progress_percentage: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee)
):
    """
    Update roadmap progress
    """
    roadmap = db.query(LearningRoadmap).filter(
        LearningRoadmap.id == roadmap_id,
        LearningRoadmap.user_id == current_user.id
    ).first()
    
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    roadmap.progress_percentage = progress_percentage
    
    # Update status based on progress
    if progress_percentage == 0:
        roadmap.status = RoadmapStatus.NOT_STARTED
    elif progress_percentage >= 100:
        roadmap.status = RoadmapStatus.COMPLETED
        from datetime import datetime
        roadmap.completed_at = datetime.utcnow()
    else:
        roadmap.status = RoadmapStatus.IN_PROGRESS
        if not roadmap.started_at:
            from datetime import datetime
            roadmap.started_at = datetime.utcnow()
    
    db.commit()
    db.refresh(roadmap)
    
    return {"message": "Progress updated successfully", "roadmap": roadmap}


@router.get("/roadmaps/{roadmap_id}", response_model=LearningRoadmapResponse)
def get_roadmap_detail(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee)
):
    """
    Get detailed roadmap information
    """
    roadmap = db.query(LearningRoadmap).filter(
        LearningRoadmap.id == roadmap_id,
        LearningRoadmap.user_id == current_user.id
    ).first()
    
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    return roadmap


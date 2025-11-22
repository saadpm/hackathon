from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
from middleware import get_current_user, get_current_employee
from models.user import User
from models.skill import EmployeeSkill
from models.job import JobDescription
from schemas import (
    SkillsSubmitRequest, EmployeeSkillResponse,
    GapAnalysisResponse
)
from services import openai_service, vector_service

router = APIRouter(prefix="/assessment", tags=["Assessment"])


@router.post("/submit-skills", response_model=List[EmployeeSkillResponse])
def submit_skills(
    request: SkillsSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee)
):
    """
    Employee submits their current skills
    """
    # Delete existing skills for this user
    db.query(EmployeeSkill).filter(EmployeeSkill.user_id == current_user.id).delete()
    
    # Add new skills
    new_skills = []
    for skill_data in request.skills:
        skill = EmployeeSkill(
            user_id=current_user.id,
            **skill_data.dict()
        )
        db.add(skill)
        new_skills.append(skill)
    
    db.commit()
    
    # Refresh all skills
    for skill in new_skills:
        db.refresh(skill)
    
    # Add to vector database
    skills_for_vector = [
        {
            "skill_name": s.skill_name,
            "proficiency": s.proficiency_level.value,
            "experience": float(s.years_of_experience),
            "metadata": {
                "user_id": current_user.id,
                "skill_id": s.id
            }
        }
        for s in new_skills
    ]
    vector_service.add_skills_to_index(skills_for_vector)
    
    return new_skills


@router.get("/my-skills", response_model=List[EmployeeSkillResponse])
def get_my_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee)
):
    """
    Get employee's current skills
    """
    skills = db.query(EmployeeSkill).filter(EmployeeSkill.user_id == current_user.id).all()
    return skills


@router.get("/gap-analysis", response_model=GapAnalysisResponse)
def get_gap_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee)
):
    """
    Analyze skill gap between employee's skills and job requirements
    """
    # Check if user has a job title assigned
    if not current_user.job_title_id:
        raise HTTPException(status_code=400, detail="No job title assigned to user")
    
    # Get job description for user's job title
    jd = db.query(JobDescription).filter(
        JobDescription.job_title_id == current_user.job_title_id
    ).first()
    
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found for your job title")
    
    # Get employee's skills
    employee_skills = db.query(EmployeeSkill).filter(
        EmployeeSkill.user_id == current_user.id
    ).all()
    
    if not employee_skills:
        raise HTTPException(status_code=400, detail="Please submit your skills first")
    
    # Prepare data for analysis
    employee_skills_data = [
        {
            "skill_name": s.skill_name,
            "proficiency_level": s.proficiency_level.value,
            "years_of_experience": float(s.years_of_experience)
        }
        for s in employee_skills
    ]
    
    required_skills = jd.required_skills
    
    # Vector-based comparison
    vector_comparison = vector_service.compare_skill_sets(
        employee_skills_data,
        required_skills
    )
    
    # AI-based gap analysis
    ai_analysis = openai_service.analyze_skill_gap(
        employee_skills_data,
        required_skills,
        current_user.job_title.title,
        float(jd.required_years_of_experience)
    )
    
    # Combine results
    return {
        "missing_skills": ai_analysis.get("missing_skills", vector_comparison["missing_skills"]),
        "matched_skills": vector_comparison["matched_skills"],
        "skills_to_improve": ai_analysis.get("skills_to_improve", []),
        "gap_percentage": ai_analysis.get("gap_percentage", vector_comparison["gap_percentage"]),
        "priority_areas": ai_analysis.get("priority_areas", []),
        "estimated_time_to_bridge": ai_analysis.get("estimated_time_to_bridge", 0),
        "similarity_scores": vector_comparison["similarity_scores"]
    }


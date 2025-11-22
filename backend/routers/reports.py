from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database.connection import get_db
from middleware import get_current_od_manager
from models.user import User, UserRole
from models.skill import EmployeeSkill
from models.roadmap import LearningRoadmap
from models.quiz import AssessmentResult
from models.job import JobDescription, JobTitle
from schemas import EmployeeReportResponse, CareerProgressionResponse
from services import openai_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/employees", response_model=List[dict])
def list_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_od_manager)
):
    """
    List all employees with basic info (OD Manager only)
    """
    employees = db.query(User).filter(User.role == UserRole.EMPLOYEE).all()
    
    result = []
    for emp in employees:
        # Get total assessments
        total_assessments = db.query(func.count(AssessmentResult.id)).filter(
            AssessmentResult.user_id == emp.id
        ).scalar()
        
        # Get average score
        avg_score = db.query(func.avg(AssessmentResult.points_earned)).filter(
            AssessmentResult.user_id == emp.id
        ).scalar() or 0
        
        # Get skill count
        skill_count = db.query(func.count(EmployeeSkill.id)).filter(
            EmployeeSkill.user_id == emp.id
        ).scalar()
        
        # Get active roadmaps
        active_roadmaps = db.query(func.count(LearningRoadmap.id)).filter(
            LearningRoadmap.user_id == emp.id,
            LearningRoadmap.status.in_(["not_started", "in_progress"])
        ).scalar()
        
        result.append({
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "job_title_id": emp.job_title_id,
            "job_title": emp.job_title.title if emp.job_title else None,
            "years_of_experience": float(emp.years_of_experience) if emp.years_of_experience else 0,
            "total_skills": skill_count,
            "total_assessments": total_assessments,
            "average_score": float(avg_score),
            "active_roadmaps": active_roadmaps
        })
    
    return result


@router.get("/employee/{employee_id}", response_model=dict)
def get_employee_report(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_od_manager)
):
    """
    Get detailed report for a specific employee (OD Manager only)
    """
    employee = db.query(User).filter(
        User.id == employee_id,
        User.role == UserRole.EMPLOYEE
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Get skills
    skills = db.query(EmployeeSkill).filter(EmployeeSkill.user_id == employee_id).all()
    
    # Get roadmaps
    roadmaps = db.query(LearningRoadmap).filter(LearningRoadmap.user_id == employee_id).all()
    
    # Get assessment results
    assessments = db.query(AssessmentResult).filter(AssessmentResult.user_id == employee_id).all()
    
    # Calculate assessment score
    if assessments:
        total_points = sum(a.points_earned for a in assessments)
        total_assessments = len(assessments)
        avg_score = total_points / total_assessments if total_assessments > 0 else 0
    else:
        avg_score = 0
        total_assessments = 0
    
    # Get gap analysis if job title exists
    gap_analysis = None
    if employee.job_title_id:
        jd = db.query(JobDescription).filter(
            JobDescription.job_title_id == employee.job_title_id
        ).first()
        
        if jd and skills:
            employee_skills_data = [
                {
                    "skill_name": s.skill_name,
                    "proficiency_level": s.proficiency_level.value,
                    "years_of_experience": float(s.years_of_experience)
                }
                for s in skills
            ]
            
            ai_analysis = openai_service.analyze_skill_gap(
                employee_skills_data,
                jd.required_skills,
                employee.job_title.title,
                float(jd.required_years_of_experience)
            )
            
            gap_analysis = ai_analysis
    
    return {
        "user": {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "role": employee.role.value,
            "job_title_id": employee.job_title_id,
            "job_title": employee.job_title.title if employee.job_title else None,
            "years_of_experience": float(employee.years_of_experience) if employee.years_of_experience else 0
        },
        "skills": [
            {
                "id": s.id,
                "skill_name": s.skill_name,
                "proficiency_level": s.proficiency_level.value,
                "years_of_experience": float(s.years_of_experience),
                "self_assessment_score": s.self_assessment_score,
                "is_verified": s.is_verified
            }
            for s in skills
        ],
        "gap_analysis": gap_analysis,
        "roadmaps": [
            {
                "id": r.id,
                "skill_name": r.skill_name,
                "current_level": r.current_level.value if r.current_level else None,
                "target_level": r.target_level.value,
                "status": r.status.value,
                "progress_percentage": float(r.progress_percentage)
            }
            for r in roadmaps
        ],
        "assessment_score": avg_score,
        "total_assessments": total_assessments
    }


@router.get("/career-progression/{employee_id}", response_model=CareerProgressionResponse)
def get_career_progression(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_od_manager)
):
    """
    Get career progression suggestions for an employee (OD Manager only)
    """
    employee = db.query(User).filter(
        User.id == employee_id,
        User.role == UserRole.EMPLOYEE
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if not employee.job_title_id:
        raise HTTPException(status_code=400, detail="Employee has no job title assigned")
    
    # Get current job title
    current_job = db.query(JobTitle).filter(JobTitle.id == employee.job_title_id).first()
    
    # Get next level jobs
    next_jobs = []
    if current_job.next_level_job_id:
        next_job = db.query(JobTitle).filter(JobTitle.id == current_job.next_level_job_id).first()
        if next_job:
            next_jobs.append(next_job.title)
    
    # Get employee skills
    skills = db.query(EmployeeSkill).filter(EmployeeSkill.user_id == employee_id).all()
    current_skills = [s.skill_name for s in skills]
    
    if not next_jobs:
        return {
            "current_job_title": current_job.title,
            "recommended_next_role": None,
            "readiness_percentage": 100.0,
            "reasons": ["Already at highest level"],
            "skills_needed": [],
            "estimated_timeline_months": 0
        }
    
    # Use OpenAI to suggest career progression
    progression = openai_service.suggest_career_progression(
        current_job_title=current_job.title,
        current_skills=current_skills,
        years_of_experience=float(employee.years_of_experience),
        available_next_roles=next_jobs
    )
    
    return {
        "current_job_title": current_job.title,
        "recommended_next_role": progression.get("recommended_role"),
        "readiness_percentage": progression.get("readiness_percentage", 0),
        "reasons": progression.get("reasons", []),
        "skills_needed": progression.get("skills_needed", []),
        "estimated_timeline_months": progression.get("timeline", 0)
    }


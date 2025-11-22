from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
from middleware import get_current_user, get_current_od_manager
from models.user import User
from models.job import JobTitle, JobDescription
from schemas import (
    JobTitleCreate, JobTitleUpdate, JobTitleResponse,
    JobDescriptionCreate, JobDescriptionUpdate, JobDescriptionResponse
)

router = APIRouter(prefix="/job", tags=["Job Management"])


# Job Titles
@router.get("/titles", response_model=List[JobTitleResponse])
def list_job_titles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all job titles with career progression paths
    """
    job_titles = db.query(JobTitle).all()
    return job_titles


@router.post("/titles", response_model=JobTitleResponse)
def create_job_title(
    request: JobTitleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_od_manager)
):
    """
    Create a new job title (OD Manager only)
    """
    job_title = JobTitle(**request.dict())
    db.add(job_title)
    db.commit()
    db.refresh(job_title)
    return job_title


@router.put("/titles/{job_title_id}", response_model=JobTitleResponse)
def update_job_title(
    job_title_id: int,
    request: JobTitleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_od_manager)
):
    """
    Update job title (OD Manager only)
    """
    job_title = db.query(JobTitle).filter(JobTitle.id == job_title_id).first()
    if not job_title:
        raise HTTPException(status_code=404, detail="Job title not found")
    
    for key, value in request.dict(exclude_unset=True).items():
        setattr(job_title, key, value)
    
    db.commit()
    db.refresh(job_title)
    return job_title


# Job Descriptions
@router.get("/descriptions", response_model=List[JobDescriptionResponse])
def list_job_descriptions(
    job_title_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List job descriptions, optionally filtered by job title
    """
    query = db.query(JobDescription)
    if job_title_id:
        query = query.filter(JobDescription.job_title_id == job_title_id)
    
    return query.all()


@router.post("/descriptions", response_model=JobDescriptionResponse)
def create_job_description(
    request: JobDescriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_od_manager)
):
    """
    Create job description (OD Manager only)
    """
    # Check if job title exists
    job_title = db.query(JobTitle).filter(JobTitle.id == request.job_title_id).first()
    if not job_title:
        raise HTTPException(status_code=404, detail="Job title not found")
    
    jd = JobDescription(**request.dict())
    db.add(jd)
    db.commit()
    db.refresh(jd)
    return jd


@router.put("/descriptions/{jd_id}", response_model=JobDescriptionResponse)
def update_job_description(
    jd_id: int,
    request: JobDescriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_od_manager)
):
    """
    Update job description (OD Manager only)
    """
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    for key, value in request.dict(exclude_unset=True).items():
        setattr(jd, key, value)
    
    db.commit()
    db.refresh(jd)
    return jd


@router.get("/descriptions/{jd_id}", response_model=JobDescriptionResponse)
def get_job_description(
    jd_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get specific job description
    """
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    return jd


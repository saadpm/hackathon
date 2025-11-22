from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from models.user import UserRole
from models.skill import ProficiencyLevel
from models.roadmap import RoadmapStatus


# Auth Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.EMPLOYEE


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


# User Schemas
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    job_title_id: Optional[int]
    years_of_experience: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# Job Title Schemas
class JobTitleCreate(BaseModel):
    title: str
    level: int
    next_level_job_id: Optional[int] = None
    department: Optional[str] = None


class JobTitleUpdate(BaseModel):
    title: Optional[str] = None
    level: Optional[int] = None
    next_level_job_id: Optional[int] = None
    department: Optional[str] = None


class JobTitleResponse(BaseModel):
    id: int
    title: str
    level: int
    next_level_job_id: Optional[int]
    department: Optional[str]
    
    class Config:
        from_attributes = True


# Job Description Schemas
class JobDescriptionCreate(BaseModel):
    job_title_id: int
    required_skills: List[str]
    required_tools: List[str]
    required_years_of_experience: float
    competency_weightage: Optional[Dict[str, float]] = None
    expected_proficiency_levels: Optional[Dict[str, str]] = None
    preferred_skills: Optional[List[str]] = None
    description: Optional[str] = None


class JobDescriptionUpdate(BaseModel):
    required_skills: Optional[List[str]] = None
    required_tools: Optional[List[str]] = None
    required_years_of_experience: Optional[float] = None
    competency_weightage: Optional[Dict[str, float]] = None
    expected_proficiency_levels: Optional[Dict[str, str]] = None
    preferred_skills: Optional[List[str]] = None
    description: Optional[str] = None


class JobDescriptionResponse(BaseModel):
    id: int
    job_title_id: int
    required_skills: List[str]
    required_tools: List[str]
    required_years_of_experience: float
    competency_weightage: Optional[Dict[str, float]]
    expected_proficiency_levels: Optional[Dict[str, str]]
    preferred_skills: Optional[List[str]]
    description: Optional[str]
    
    class Config:
        from_attributes = True


# Skill Schemas
class SkillSubmit(BaseModel):
    skill_name: str
    proficiency_level: ProficiencyLevel
    years_of_experience: float
    self_assessment_score: Optional[int] = None


class SkillsSubmitRequest(BaseModel):
    skills: List[SkillSubmit]


class EmployeeSkillResponse(BaseModel):
    id: int
    skill_name: str
    proficiency_level: ProficiencyLevel
    years_of_experience: float
    self_assessment_score: Optional[int]
    is_verified: bool
    
    class Config:
        from_attributes = True


# Quiz Schemas
class QuizQuestionGenerate(BaseModel):
    job_title_id: int
    skill_name: str
    experience_level_years: float
    difficulty_level: ProficiencyLevel
    num_questions: int = 5


class QuizQuestionResponse(BaseModel):
    id: int
    job_title_id: int
    skill_name: str
    question_text: str
    options: Dict[str, str]
    difficulty_level: ProficiencyLevel
    experience_level_years: Optional[float]
    points: int
    
    class Config:
        from_attributes = True


class QuizAnswerSubmit(BaseModel):
    quiz_question_id: int
    selected_answer: str
    time_taken_seconds: Optional[int] = None


class QuizSubmitRequest(BaseModel):
    answers: List[QuizAnswerSubmit]


class AssessmentResultResponse(BaseModel):
    id: int
    quiz_question_id: int
    selected_answer: str
    is_correct: bool
    points_earned: int
    attempted_at: datetime
    
    class Config:
        from_attributes = True


# Gap Analysis Schemas
class GapAnalysisResponse(BaseModel):
    missing_skills: List[str]
    matched_skills: List[str]
    skills_to_improve: List[str]
    gap_percentage: float
    priority_areas: List[str]
    estimated_time_to_bridge: int
    similarity_scores: Dict[str, Any]


# Roadmap Schemas
class RoadmapGenerateRequest(BaseModel):
    skill_name: str
    target_level: ProficiencyLevel


class LearningRoadmapResponse(BaseModel):
    id: int
    skill_name: str
    current_level: Optional[ProficiencyLevel]
    target_level: ProficiencyLevel
    gap_percentage: Optional[float]
    milestones: List[Dict[str, Any]]
    course_recommendations: Optional[List[Dict[str, Any]]]
    practice_tasks: Optional[List[Dict[str, Any]]]
    estimated_completion_weeks: Optional[int]
    status: RoadmapStatus
    progress_percentage: float
    
    class Config:
        from_attributes = True


# Report Schemas
class EmployeeReportResponse(BaseModel):
    user: UserResponse
    skills: List[EmployeeSkillResponse]
    gap_analysis: Optional[GapAnalysisResponse]
    roadmaps: List[LearningRoadmapResponse]
    assessment_score: Optional[float]
    total_assessments: int


class CareerProgressionResponse(BaseModel):
    current_job_title: str
    recommended_next_role: Optional[str]
    readiness_percentage: float
    reasons: List[str]
    skills_needed: List[str]
    estimated_timeline_months: int


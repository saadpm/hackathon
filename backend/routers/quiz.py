from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
from middleware import get_current_user, get_current_od_manager, get_current_employee
from models.user import User
from models.quiz import QuizQuestion, AssessmentResult
from models.job import JobTitle
from schemas import (
    QuizQuestionGenerate, QuizQuestionResponse,
    QuizSubmitRequest, AssessmentResultResponse
)
from services import openai_service

router = APIRouter(prefix="/quiz", tags=["Quiz & Assessment"])


@router.post("/generate")
def generate_quiz(
    request: QuizQuestionGenerate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_od_manager)
):
    """
    Generate quiz questions using OpenAI (OD Manager only)
    """
    # Get job title
    job_title = db.query(JobTitle).filter(JobTitle.id == request.job_title_id).first()
    if not job_title:
        raise HTTPException(status_code=404, detail="Job title not found")
    
    # Generate questions using OpenAI
    generated_questions = openai_service.generate_quiz_questions(
        skill_name=request.skill_name,
        job_title=job_title.title,
        experience_level_years=request.experience_level_years,
        difficulty_level=request.difficulty_level.value,
        num_questions=request.num_questions
    )
    
    if not generated_questions:
        raise HTTPException(status_code=500, detail="Failed to generate quiz questions")
    
    # Save questions to database
    saved_questions = []
    for q in generated_questions:
        quiz_question = QuizQuestion(
            job_title_id=request.job_title_id,
            skill_name=request.skill_name,
            question_text=q.get("question_text", ""),
            options=q.get("options", {}),
            correct_answer=q.get("correct_answer", ""),
            difficulty_level=request.difficulty_level,
            experience_level_years=request.experience_level_years,
            explanation=q.get("explanation", ""),
            created_by=current_user.id,
            is_active=True
        )
        db.add(quiz_question)
        saved_questions.append(quiz_question)
    
    db.commit()
    
    # Refresh all questions
    for q in saved_questions:
        db.refresh(q)
    
    return {
        "message": f"Successfully generated {len(saved_questions)} quiz questions",
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "explanation": q.explanation
            }
            for q in saved_questions
        ]
    }


@router.get("/questions", response_model=List[QuizQuestionResponse])
def get_quiz_questions(
    job_title_id: int = None,
    skill_name: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get quiz questions (filtered by job title and/or skill)
    """
    query = db.query(QuizQuestion).filter(QuizQuestion.is_active == True)
    
    if job_title_id:
        query = query.filter(QuizQuestion.job_title_id == job_title_id)
    
    if skill_name:
        query = query.filter(QuizQuestion.skill_name == skill_name)
    
    # For employees, only show questions for their job title
    if current_user.role.value == "EMPLOYEE":
        if not current_user.job_title_id:
            raise HTTPException(status_code=400, detail="No job title assigned")
        query = query.filter(QuizQuestion.job_title_id == current_user.job_title_id)
    
    questions = query.all()
    
    # Don't send correct answer to employees
    if current_user.role.value == "EMPLOYEE":
        return [
            {
                "id": q.id,
                "job_title_id": q.job_title_id,
                "skill_name": q.skill_name,
                "question_text": q.question_text,
                "options": q.options,
                "difficulty_level": q.difficulty_level,
                "experience_level_years": q.experience_level_years,
                "points": q.points
            }
            for q in questions
        ]
    
    return questions


@router.post("/submit", response_model=dict)
def submit_quiz(
    request: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee)
):
    """
    Submit quiz answers (Employee only)
    """
    results = []
    total_score = 0
    total_points = 0
    
    for answer in request.answers:
        # Get the question
        question = db.query(QuizQuestion).filter(
            QuizQuestion.id == answer.quiz_question_id
        ).first()
        
        if not question:
            continue
        
        # Check if answer is correct
        is_correct = answer.selected_answer == question.correct_answer
        points_earned = question.points if is_correct else 0
        
        # Save result
        result = AssessmentResult(
            user_id=current_user.id,
            quiz_question_id=answer.quiz_question_id,
            selected_answer=answer.selected_answer,
            is_correct=is_correct,
            points_earned=points_earned,
            time_taken_seconds=answer.time_taken_seconds
        )
        db.add(result)
        results.append(result)
        
        total_score += points_earned
        total_points += question.points
    
    db.commit()
    
    # Calculate percentage
    percentage = (total_score / total_points * 100) if total_points > 0 else 0
    
    return {
        "message": "Quiz submitted successfully",
        "total_questions": len(request.answers),
        "correct_answers": sum(1 for r in results if r.is_correct),
        "total_score": total_score,
        "total_possible_points": total_points,
        "percentage": round(percentage, 2)
    }


@router.get("/results", response_model=List[AssessmentResultResponse])
def get_my_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employee)
):
    """
    Get employee's quiz results
    """
    results = db.query(AssessmentResult).filter(
        AssessmentResult.user_id == current_user.id
    ).order_by(AssessmentResult.attempted_at.desc()).all()
    
    return results


@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_od_manager)
):
    """
    Delete or deactivate a quiz question (OD Manager only)
    """
    question = db.query(QuizQuestion).filter(QuizQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question.is_active = False
    db.commit()
    
    return {"message": "Question deactivated successfully"}


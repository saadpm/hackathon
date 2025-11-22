from typing import List, Dict, Any
from openai import OpenAI
from config import settings


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL
        )
    
    def generate_quiz_questions(
        self,
        skill_name: str,
        job_title: str,
        experience_level_years: float,
        difficulty_level: str,
        num_questions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate quiz questions using OpenAI based on skill and experience level
        """
        prompt = f"""Generate {num_questions} multiple-choice quiz questions to assess {skill_name} skills for a {job_title} position.

Target Experience Level: {experience_level_years} years
Difficulty Level: {difficulty_level}

For each question, provide:
1. A clear question text that tests practical knowledge
2. Four answer options (A, B, C, D)
3. The correct answer (letter)
4. A brief explanation of why that answer is correct

Format the response as a JSON array with this structure:
[
  {{
    "question_text": "Question here?",
    "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}},
    "correct_answer": "A",
    "explanation": "Explanation here"
  }}
]

Make questions relevant to {experience_level_years} years of experience and {difficulty_level} difficulty level.
Focus on practical, real-world scenarios that a {job_title} would encounter."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert technical interviewer and assessment creator. Generate high-quality, practical quiz questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Extract questions array from response
            if isinstance(result, dict) and "questions" in result:
                return result["questions"]
            elif isinstance(result, list):
                return result
            else:
                return []
                
        except Exception as e:
            print(f"Error generating quiz questions: {str(e)}")
            return []
    
    def analyze_skill_gap(
        self,
        employee_skills: List[Dict[str, Any]],
        required_skills: List[str],
        job_title: str,
        required_experience_years: float
    ) -> Dict[str, Any]:
        """
        Use OpenAI to analyze skill gaps and provide insights
        """
        employee_skills_str = ", ".join([
            f"{s['skill_name']} ({s['proficiency_level']}, {s['years_of_experience']}y)"
            for s in employee_skills
        ])
        
        required_skills_str = ", ".join(required_skills)
        
        prompt = f"""Analyze the skill gap for an employee aspiring to be a {job_title} (requires {required_experience_years} years experience).

Employee's Current Skills:
{employee_skills_str}

Required Skills for {job_title}:
{required_skills_str}

Provide a JSON response with:
1. "missing_skills": Array of skills the employee lacks
2. "skills_to_improve": Array of skills where proficiency needs improvement
3. "gap_percentage": Overall gap as a percentage (0-100)
4. "priority_areas": Top 3 skills to focus on first
5. "estimated_time_to_bridge": Estimated weeks to bridge the gap with dedicated learning

Be realistic and specific."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a career development expert specializing in skill gap analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error analyzing skill gap: {str(e)}")
            return {
                "missing_skills": [],
                "skills_to_improve": [],
                "gap_percentage": 0,
                "priority_areas": [],
                "estimated_time_to_bridge": 0
            }
    
    def generate_learning_roadmap(
        self,
        skill_name: str,
        current_level: str,
        target_level: str,
        gap_percentage: float,
        job_title: str
    ) -> Dict[str, Any]:
        """
        Generate a personalized learning roadmap using OpenAI
        """
        prompt = f"""Create a detailed learning roadmap for improving {skill_name} skills.

Current Level: {current_level}
Target Level: {target_level}
Skill Gap: {gap_percentage}%
Goal: To work as a {job_title}

Provide a JSON response with:
1. "milestones": Array of weekly/monthly learning milestones with specific goals
2. "course_recommendations": Array of recommended courses with:
   - "platform": (YouTube, Udemy, Coursera, etc.)
   - "title": Course title
   - "url": Course URL (use real, popular courses)
   - "duration": Estimated hours
   - "difficulty": beginner/intermediate/advanced
3. "practice_tasks": Array of practical projects/exercises to complete
4. "estimated_completion_weeks": Total weeks to complete
5. "daily_time_commitment": Recommended hours per day

Make recommendations specific, actionable, and realistic."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a learning and development expert who creates personalized learning roadmaps."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating learning roadmap: {str(e)}")
            return {
                "milestones": [],
                "course_recommendations": [],
                "practice_tasks": [],
                "estimated_completion_weeks": 0,
                "daily_time_commitment": 0
            }
    
    def suggest_career_progression(
        self,
        current_job_title: str,
        current_skills: List[str],
        years_of_experience: float,
        available_next_roles: List[str]
    ) -> Dict[str, Any]:
        """
        Suggest next career step based on current skills and experience
        """
        skills_str = ", ".join(current_skills)
        roles_str = ", ".join(available_next_roles)
        
        prompt = f"""Analyze career progression options for an employee.

Current Role: {current_job_title}
Years of Experience: {years_of_experience}
Current Skills: {skills_str}

Available Next Level Roles:
{roles_str}

Provide a JSON response with:
1. "recommended_role": The best next role to target
2. "readiness_percentage": How ready they are (0-100)
3. "reasons": Array of reasons for this recommendation
4. "skills_needed": Array of additional skills needed for the role
5. "timeline": Estimated months until ready

Be honest and constructive."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a career counselor specializing in software development career paths."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error suggesting career progression: {str(e)}")
            return {
                "recommended_role": "",
                "readiness_percentage": 0,
                "reasons": [],
                "skills_needed": [],
                "timeline": 0
            }


# Singleton instance
openai_service = OpenAIService()


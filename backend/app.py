from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import auth, job, assessment, quiz, roadmap, reports

# Create FastAPI app
app = FastAPI(
    title="SkillPilot AI",
    description="Intelligent Learning Experience Platform (LMS) for Software Development",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(job.router, prefix="/api")
app.include_router(assessment.router, prefix="/api")
app.include_router(quiz.router, prefix="/api")
app.include_router(roadmap.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SkillPilot AI - Intelligent Learning Experience Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SkillPilot AI Backend"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True
    )


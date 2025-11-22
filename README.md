# 🎯 SkillPilot AI - Intelligent Learning Experience Platform

SkillPilot AI is a comprehensive Learning Management System (LMS) designed for software development companies to assess employee skills, identify gaps, and provide personalized learning roadmaps.

## 🌟 Features

### For Employees
- **Skill Assessment**: Submit and manage your current skillset
- **Gap Analysis**: AI-powered comparison against job requirements using vector embeddings
- **Intelligent Quizzes**: Take AI-generated quizzes tailored to your experience level
- **Learning Roadmap**: Get personalized learning paths with course recommendations from YouTube, Udemy, Coursera
- **Career Progression**: Track progress toward next career level

### For OD Managers
- **Employee Management**: View and manage all employees
- **Job Management**: Create and manage job titles with career progression paths
- **Job Description Management**: Define required skills, tools, and experience levels
- **Quiz Generation**: Generate assessment quizzes using OpenAI
- **Reports & Analytics**: View employee progress, gaps, and readiness for promotion

## 🏗️ Architecture

### Backend (FastAPI + Python)
- **FastAPI**: High-performance REST API
- **MySQL**: Relational database for structured data
- **FAISS**: Vector database for skill embeddings and semantic search
- **OpenAI**: AI-powered quiz generation, gap analysis, and roadmap creation
- **JWT Authentication**: Secure role-based access control (RBAC)

### Frontend (HTML + JavaScript)
- **Vanilla JavaScript**: No framework dependencies
- **Responsive Design**: Modern, mobile-friendly UI
- **Role-based UI**: Different interfaces for OD Managers and Employees

### Infrastructure
- **Docker Compose**: Easy deployment and orchestration
- **Nginx**: Reverse proxy for frontend

## 📋 Prerequisites

- Docker and Docker Compose
- OpenAI API key (or compatible API)
- At least 4GB RAM for running all services

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hackathon
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp env.example .env
```

Edit `.env` and add your OpenAI credentials:

```env
OPENAI_API_KEY=your-actual-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3. Start the Application

```bash
docker-compose up -d
```

This will start:
- **MySQL Database** on port 3306
- **Backend API** on port 8000
- **Frontend** on port 80

### 4. Access the Application

Open your browser and navigate to:

```
http://localhost
```

### Demo Credentials

**OD Manager:**
- Email: `admin@skillpilot.com`
- Password: `admin123`

**Employee:**
- Email: `john.doe@skillpilot.com`
- Password: `admin123`

## 📊 Database Schema

The application uses 7 main tables:

1. **users** - User accounts with role-based access
2. **job_titles** - Job titles with career progression linking
3. **job_descriptions** - Detailed JD with required skills and experience
4. **employee_skills** - Employee skill assessments
5. **quiz_questions** - AI-generated assessment questions
6. **assessment_results** - Quiz submission results
7. **learning_roadmaps** - Personalized learning paths

## 🔧 Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt
```

Create `.env` file and run:

```bash
uvicorn app:app --reload
```

API will be available at `http://localhost:8000`
API Documentation at `http://localhost:8000/docs`

### Frontend Development

The frontend is static HTML/JS. Simply open `frontend/index.html` in a browser or use:

```bash
cd frontend
python -m http.server 3000
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - Register new user (OD Manager only)

### Job Management
- `GET /api/job/titles` - List all job titles
- `POST /api/job/titles` - Create job title (OD Manager)
- `GET /api/job/descriptions` - List job descriptions
- `POST /api/job/descriptions` - Create JD (OD Manager)

### Assessment
- `POST /api/assessment/submit-skills` - Submit employee skills
- `GET /api/assessment/my-skills` - Get employee's skills
- `GET /api/assessment/gap-analysis` - Get AI-powered gap analysis

### Quiz
- `POST /api/quiz/generate` - Generate quiz using OpenAI (OD Manager)
- `GET /api/quiz/questions` - Get quiz questions
- `POST /api/quiz/submit` - Submit quiz answers (Employee)
- `GET /api/quiz/results` - Get assessment results

### Roadmap
- `POST /api/roadmap/generate` - Generate learning roadmap
- `GET /api/roadmap/my-roadmaps` - Get employee's roadmaps
- `PUT /api/roadmap/roadmaps/{id}/progress` - Update progress

### Reports
- `GET /api/reports/employees` - List all employees (OD Manager)
- `GET /api/reports/employee/{id}` - Get detailed employee report
- `GET /api/reports/career-progression/{id}` - Get career progression suggestions

## 🧠 AI Features

### 1. Skill Gap Analysis
- Uses **FAISS vector embeddings** to compare employee skills with job requirements
- **OpenAI** provides contextual gap analysis with priorities
- Combines vector similarity scores with AI insights

### 2. Quiz Generation
- **OpenAI GPT-4** generates questions based on:
  - Skill name
  - Job title
  - Experience level (years)
  - Difficulty level
- Questions are tailored to real-world scenarios

### 3. Learning Roadmap
- AI-generated weekly/monthly milestones
- Course recommendations from popular platforms
- Practical tasks and projects
- Estimated completion time

### 4. Career Progression
- AI suggests next career steps
- Assesses readiness percentage
- Lists required skills for promotion

## 🔒 Security

- **JWT-based authentication** with secure token management
- **Role-Based Access Control (RBAC)** - OD Manager vs Employee
- **Password hashing** using bcrypt
- **API authentication** required for all protected endpoints

## 📦 Project Structure

```
hackathon/
├── backend/
│   ├── app.py                 # Main FastAPI application
│   ├── config.py              # Configuration management
│   ├── schemas.py             # Pydantic schemas
│   ├── database/
│   │   └── connection.py      # Database setup
│   ├── models/                # SQLAlchemy models
│   │   ├── user.py
│   │   ├── job.py
│   │   ├── skill.py
│   │   ├── quiz.py
│   │   └── roadmap.py
│   ├── middleware/            # Auth middleware
│   │   └── auth.py
│   ├── routers/               # API routes
│   │   ├── auth.py
│   │   ├── job.py
│   │   ├── assessment.py
│   │   ├── quiz.py
│   │   ├── roadmap.py
│   │   └── reports.py
│   └── services/              # Business logic
│       ├── openai_service.py
│       └── vector_service.py
├── frontend/
│   ├── index.html             # Login page
│   ├── dashboard.html         # Main dashboard
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── config.js
│       ├── auth.js
│       ├── api.js
│       ├── login.js
│       └── dashboard.js
├── database/
│   └── init.sql               # Database schema and seed data
├── docker-compose.yml         # Docker orchestration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🧪 Testing

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@skillpilot.com","password":"admin123"}'
```

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check if MySQL is running
docker-compose ps

# View MySQL logs
docker-compose logs mysql

# Reset database
docker-compose down -v
docker-compose up -d
```

### Backend Issues

```bash
# View backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### OpenAI API Issues

- Verify your API key in `.env` file
- Check API quota and rate limits
- Ensure `OPENAI_BASE_URL` is correct

## 🎨 Customization

### Adding New Skills

Skills are dynamically managed by employees and compared using vector embeddings. No hardcoding needed.

### Modifying Job Levels

Job titles can be linked for career progression through the OD Manager panel.

### Custom Quiz Templates

Quizzes are generated by OpenAI on-demand. Modify prompts in `backend/services/openai_service.py`.

## 📈 Future Enhancements

- [ ] Real-time notifications for quiz assignments
- [ ] Video course integration
- [ ] Peer skill endorsements
- [ ] Gamification with badges and leaderboards
- [ ] Integration with HR systems
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Skill marketplace for internal projects

## 📝 License

This project is developed for hackathon purposes.

## 👥 Contributors

Built with ❤️ for the hackathon

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- OpenAI for GPT-4 API
- FAISS for vector similarity search
- All open-source contributors

---

For issues or questions, please open an issue on GitHub or contact the development team.

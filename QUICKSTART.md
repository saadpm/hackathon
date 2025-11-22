# ⚡ SkillPilot AI - Quick Start Guide

## 🎯 What is SkillPilot AI?

An AI-powered Learning Management System that:
- ✅ Assesses employee skills
- 📊 Identifies skill gaps using AI and vector embeddings
- 🧪 Generates custom quizzes with OpenAI
- 🗺️ Creates personalized learning roadmaps
- 📈 Tracks career progression

---

## 🚀 Get Started in 3 Minutes

### Step 1: Update OpenAI Credentials (30 seconds)

Edit the `.env` file:

```bash
OPENAI_API_KEY=sk-your-actual-openai-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Step 2: Start the Application (1 minute)

```bash
./run.sh
```

Or on Windows:
```bash
docker-compose up -d
```

### Step 3: Login (30 seconds)

Open http://localhost in your browser

**OD Manager Login:**
- Email: `admin@skillpilot.com`
- Password: `admin123`

**Employee Login:**
- Email: `john.doe@skillpilot.com`  
- Password: `admin123`

---

## 🎮 Quick Tour

### As an Employee:

1. **Add Your Skills**
   - Go to "My Skills"
   - Add skills with proficiency levels
   - Save

2. **View Gap Analysis**
   - Go to "Gap Analysis"
   - See what skills you're missing
   - Get AI recommendations

3. **Take a Quiz**
   - Go to "Take Quiz"
   - Answer questions
   - See your score

4. **Get Learning Roadmap**
   - Go to "Learning Roadmap"
   - Generate personalized learning path
   - See course recommendations from YouTube, Udemy, Coursera

### As an OD Manager:

1. **View All Employees**
   - Dashboard shows all employees
   - See their skills, assessments, progress

2. **Manage Job Descriptions**
   - Create job titles with levels
   - Link career progression
   - Define required skills

3. **Generate Quizzes**
   - Click "Generate Quiz"
   - Select job title and skill
   - AI creates custom questions
   - Review and assign to employees

4. **View Reports**
   - Click on any employee
   - See detailed skill gap analysis
   - Track learning progress
   - Get career readiness reports

---

## 🔑 Key Features Explained

### 🧠 AI Gap Analysis

Uses two methods:
1. **Vector Embeddings (FAISS)**: Semantic similarity between skills
2. **OpenAI GPT-4**: Contextual analysis with priorities

### 📝 Smart Quiz Generation

- AI generates questions based on job role and experience
- Questions are tailored to real-world scenarios
- Automatic grading and feedback

### 🗺️ Personalized Roadmaps

- Weekly/monthly learning milestones
- Real course recommendations (YouTube, Udemy, Coursera)
- Practical projects and tasks
- Estimated completion time

### 📊 Career Progression

- AI suggests next career step
- Shows readiness percentage
- Lists skills needed for promotion
- Provides timeline estimate

---

## 📱 Main Screens

### Employee Dashboard
```
┌─────────────────────────────────────┐
│  Dashboard                          │
├─────────────────────────────────────┤
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │  5  │ │  2  │ │  1  │ │  3  │  │
│  │Skills│ │Road-│ │Comp-│ │Asses│  │
│  │     │ │maps │ │leted│ │ment │  │
│  └─────┘ └─────┘ └─────┘ └─────┘  │
│                                     │
│  Quick Actions:                     │
│  [Update Skills] [View Gaps]        │
│  [Take Quiz] [View Roadmap]         │
└─────────────────────────────────────┘
```

### OD Manager Dashboard
```
┌─────────────────────────────────────┐
│  Employee Management                │
├─────────────────────────────────────┤
│  Name     | Job      | Skills | ... │
│  John Doe | MERN Dev |   5    | ... │
│  Jane S.  | Python   |   8    | ... │
│                                     │
│  [View Report] [Career Progress]    │
└─────────────────────────────────────┘
```

---

## 🔧 Common Tasks

### Add a New Job Title

1. Login as OD Manager
2. Go to "Job Titles"
3. Click "Add Job Title"
4. Enter details and career progression
5. Save

### Create Job Description

1. Go to "Job Descriptions"
2. Select job title
3. Add required skills (JSON array)
4. Set experience requirements
5. Save

### Generate Assessment Quiz

1. Go to "Generate Quiz"
2. Select job title
3. Enter skill name
4. Choose experience level
5. Click "Generate with AI"
6. Review questions
7. Approve and assign

### View Employee Progress

1. Go to "Employees"
2. Click on employee name
3. See:
   - Current skills
   - Gap analysis
   - Assessment scores
   - Active roadmaps

---

## 💡 Pro Tips

1. **Start with Skills**: Employees should add their skills first
2. **Assign Job Titles**: Make sure employees have job titles assigned
3. **Use AI Wisely**: Quiz generation uses OpenAI tokens (costs money)
4. **Track Progress**: Update roadmap progress regularly
5. **Career Paths**: Link job titles to create progression paths

---

## 🆘 Need Help?

### App Not Starting?
```bash
docker-compose down
docker-compose up -d
docker-compose logs -f
```

### Can't Login?
- Check if backend is running: `curl http://localhost:8000/health`
- Try demo credentials above
- Reset: `docker-compose restart backend`

### Quiz Generation Not Working?
- Check OpenAI API key in `.env`
- Verify `OPENAI_BASE_URL` is correct
- Check API quota/credits

### No Gap Analysis?
- Add skills first (My Skills page)
- Make sure job title is assigned
- Check if job description exists for the role

---

## 📚 Learn More

- Full documentation: [README.md](README.md)
- Installation guide: [INSTALLATION.md](INSTALLATION.md)
- API documentation: http://localhost:8000/docs

---

## 🎉 You're Ready!

Start exploring SkillPilot AI and transform your team's learning journey!

**Happy Learning! 🚀**


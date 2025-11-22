# 🚀 SkillPilot AI - Installation Guide

## Quick Start (Recommended)

### Prerequisites
- Docker Desktop installed and running
- At least 4GB RAM available
- Internet connection

### Step 1: Configure API Keys

Edit the `.env` file and add your OpenAI credentials:

```bash
OPENAI_API_KEY=your-actual-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Step 2: Start the Application

**On Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**On Windows:**
```bash
docker-compose up -d
```

### Step 3: Access the Application

Open your browser and go to:
- **Frontend:** http://localhost
- **API Docs:** http://localhost:8000/docs

### Step 4: Login

Use these demo credentials:

**OD Manager:**
- Email: `admin@skillpilot.com`
- Password: `admin123`

**Employee:**
- Email: `john.doe@skillpilot.com`
- Password: `admin123`

---

## Manual Installation (Without Docker)

### Backend Setup

1. **Install Python 3.11+**

2. **Create virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r ../requirements.txt
```

4. **Install and configure MySQL:**
```bash
# Install MySQL 8.0
# Create database
mysql -u root -p
CREATE DATABASE skillpilot_db;
CREATE USER 'skillpilot'@'localhost' IDENTIFIED BY 'skillpilot123';
GRANT ALL PRIVILEGES ON skillpilot_db.* TO 'skillpilot'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Import schema
mysql -u skillpilot -p skillpilot_db < ../database/init.sql
```

5. **Configure environment:**
Create `.env` in the root directory with:
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=skillpilot
MYSQL_PASSWORD=skillpilot123
MYSQL_DATABASE=skillpilot_db
JWT_SECRET_KEY=change-this-to-random-string
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
VECTOR_DB_PATH=./vector_store
APP_HOST=0.0.0.0
APP_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

6. **Run backend:**
```bash
cd backend
uvicorn app:app --reload
```

Backend will run on http://localhost:8000

### Frontend Setup

1. **Install a simple HTTP server (optional):**
```bash
# Using Python
cd frontend
python -m http.server 3000

# Or using Node.js
npx http-server -p 3000
```

2. **Or just open in browser:**
```bash
# Open frontend/index.html directly in browser
# Update js/config.js to point to http://localhost:8000/api
```

---

## Verification

### Test Backend

```bash
# Health check
curl http://localhost:8000/health

# Should return: {"status":"healthy","service":"SkillPilot AI Backend"}
```

### Test Database

```bash
# Check if tables are created
docker-compose exec mysql mysql -u skillpilot -pskillpilot123 skillpilot_db -e "SHOW TABLES;"

# Should show: users, job_titles, job_descriptions, employee_skills, quiz_questions, assessment_results, learning_roadmaps
```

### Test Frontend

Open http://localhost in browser. You should see the login page.

---

## Troubleshooting

### Port Already in Use

If port 80, 3306, or 8000 is already in use:

**Option 1: Stop conflicting services**
```bash
# On Linux/Mac
sudo lsof -i :80
sudo lsof -i :3306
sudo lsof -i :8000

# On Windows
netstat -ano | findstr :80
netstat -ano | findstr :3306
netstat -ano | findstr :8000
```

**Option 2: Change ports in docker-compose.yml**
```yaml
services:
  mysql:
    ports:
      - "3307:3306"  # Change 3306 to 3307
  backend:
    ports:
      - "8001:8000"  # Change 8000 to 8001
  frontend:
    ports:
      - "8080:80"    # Change 80 to 8080
```

### Database Connection Failed

```bash
# Check if MySQL is running
docker-compose ps

# View logs
docker-compose logs mysql

# Restart MySQL
docker-compose restart mysql

# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
```

### OpenAI API Errors

1. **Invalid API Key:**
   - Check `.env` file
   - Ensure `OPENAI_API_KEY` is correct
   - No quotes around the key

2. **Rate Limit Exceeded:**
   - Wait a few minutes
   - Check your OpenAI account quota

3. **Custom API URL:**
   - If using a different OpenAI-compatible API
   - Update `OPENAI_BASE_URL` in `.env`

### Backend Won't Start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Missing dependencies - rebuild:
docker-compose build backend

# 2. Database not ready - wait 30 seconds and restart:
docker-compose restart backend

# 3. Port conflict - change port in docker-compose.yml
```

### Frontend Can't Connect to Backend

1. **Check backend is running:**
```bash
curl http://localhost:8000/health
```

2. **CORS issues:**
   - Check `CORS_ORIGINS` in `.env`
   - Add your frontend URL

3. **API URL wrong:**
   - Check `frontend/js/config.js`
   - Ensure `API_BASE_URL` points to backend

---

## Development Mode

### Backend Hot Reload

The backend automatically reloads on code changes when running with:
```bash
uvicorn app:app --reload
```

### Frontend Development

No build step needed. Just edit HTML/JS files and refresh browser.

---

## Production Deployment

### Security Checklist

- [ ] Change `JWT_SECRET_KEY` to a strong random string
- [ ] Change MySQL password
- [ ] Use HTTPS (SSL/TLS)
- [ ] Set strong CORS policy
- [ ] Enable rate limiting
- [ ] Use production OpenAI API key
- [ ] Set up database backups
- [ ] Use environment-specific `.env` files
- [ ] Enable logging and monitoring

### Production Environment Variables

```env
# Production .env
MYSQL_HOST=your-db-host
MYSQL_PASSWORD=strong-random-password
JWT_SECRET_KEY=very-strong-random-secret-min-32-chars
OPENAI_API_KEY=prod-api-key
CORS_ORIGINS=https://yourdomain.com
```

### Deploy with Docker

```bash
# Build for production
docker-compose -f docker-compose.prod.yml up -d

# Use environment file
docker-compose --env-file .env.production up -d
```

---

## Uninstall

### Remove Docker Containers

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

### Clean Manual Installation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf backend/venv

# Drop database
mysql -u root -p
DROP DATABASE skillpilot_db;
DROP USER 'skillpilot'@'localhost';
EXIT;
```

---

## Getting Help

- Check logs: `docker-compose logs -f`
- View API docs: http://localhost:8000/docs
- Check database: `docker-compose exec mysql mysql -u skillpilot -p`

For more help, refer to the main [README.md](README.md)


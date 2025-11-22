# 🚀 Running SkillPilot AI Without Docker

Since Docker requires sudo permissions, here's how to run the application directly:

## Option 1: Add Your User to Docker Group (Recommended)

Run these commands to use Docker without sudo:

```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Apply the changes (or logout/login)
newgrp docker

# Now you can run without sudo
cd /home/umair-khan/Documents/hackathon
docker-compose up -d
```

## Option 2: Run with Sudo

```bash
cd /home/umair-khan/Documents/hackathon
sudo docker-compose up -d
```

## Option 3: Run Backend Directly (No Docker)

### Step 1: Install Python Dependencies

```bash
cd /home/umair-khan/Documents/hackathon
python3 -m pip install --user -r requirements.txt
```

### Step 2: Install and Setup MySQL

```bash
# Install MySQL
sudo apt-get install mysql-server

# Start MySQL
sudo systemctl start mysql

# Create database
sudo mysql -e "CREATE DATABASE IF NOT EXISTS skillpilot_db;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'skillpilot'@'localhost' IDENTIFIED BY 'skillpilot123';"
sudo mysql -e "GRANT ALL PRIVILEGES ON skillpilot_db.* TO 'skillpilot'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Import schema
mysql -u skillpilot -pskillpilot123 skillpilot_db < database/init.sql
```

### Step 3: Run Backend

```bash
cd backend
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: http://localhost:8000

### Step 4: Serve Frontend

Open a new terminal:

```bash
cd /home/umair-khan/Documents/hackathon/frontend
python3 -m http.server 80
```

Or use port 3000 if you don't have sudo:

```bash
python3 -m http.server 3000
```

Frontend will be available at: http://localhost or http://localhost:3000

## Quick Commands

### With Docker (After Adding to Group)
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f
```

### Without Docker
```bash
# Terminal 1: Backend
cd /home/umair-khan/Documents/hackathon/backend
python3 -m uvicorn app:app --reload

# Terminal 2: Frontend
cd /home/umair-khan/Documents/hackathon/frontend
python3 -m http.server 3000
```

Then open http://localhost:8000/docs for API or http://localhost:3000 for frontend.

## Demo Credentials

**OD Manager:**
- Email: admin@skillpilot.com
- Password: admin123

**Employee:**
- Email: john.doe@skillpilot.com
- Password: admin123


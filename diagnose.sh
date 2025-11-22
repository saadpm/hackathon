#!/bin/bash

echo "🔍 SkillPilot AI - Diagnostic Tool"
echo "=================================="
echo ""

echo "1️⃣ Checking Docker containers..."
sudo docker-compose ps
echo ""

echo "2️⃣ Testing Backend Health..."
curl -s http://localhost:8000/health | jq . 2>/dev/null || curl -s http://localhost:8000/health
echo ""

echo "3️⃣ Testing Database Connection..."
sudo docker-compose exec -T mysql mysql -u skillpilot -pskillpilot123 -e "SELECT 1;" 2>&1 | grep -q "1" && echo "✅ Database connected" || echo "❌ Database connection failed"
echo ""

echo "4️⃣ Checking if tables exist..."
sudo docker-compose exec -T mysql mysql -u skillpilot -pskillpilot123 skillpilot_db -e "SHOW TABLES;" 2>&1
echo ""

echo "5️⃣ Checking if demo users exist..."
sudo docker-compose exec -T mysql mysql -u skillpilot -pskillpilot123 skillpilot_db -e "SELECT COUNT(*) as user_count FROM users;" 2>&1
echo ""

echo "6️⃣ Testing Login API..."
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@skillpilot.com","password":"admin123"}' 2>&1
echo ""

echo "7️⃣ Recent Backend Errors..."
sudo docker-compose logs backend 2>&1 | grep -i "error\|exception" | tail -10
echo ""

echo "✅ Diagnostic complete!"


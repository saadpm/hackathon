#!/bin/bash

echo "🔧 Complete Fix - Backend + CORS"
echo "================================="
echo ""

echo "1️⃣ Stopping backend..."
sudo docker-compose stop backend

echo ""
echo "2️⃣ Fixing bcrypt in container..."
sudo docker-compose run --rm backend pip install --upgrade bcrypt==4.0.1

echo ""
echo "3️⃣ Starting backend..."
sudo docker-compose up -d backend

echo ""
echo "4️⃣ Waiting for backend to start..."
sleep 10

echo ""
echo "5️⃣ Checking backend health..."
curl -s http://localhost:8000/health

echo ""
echo "6️⃣ Testing login API..."
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost" \
  -d '{"email":"admin@skillpilot.com","password":"admin123"}' \
  -v 2>&1 | grep -E "< HTTP|access-control|access_token" | head -10

echo ""
echo "7️⃣ Checking for errors..."
sudo docker-compose logs backend | tail -20

echo ""
echo "✅ Fix applied!"
echo ""
echo "🌐 Try logging in at: http://localhost"
echo "   Email: admin@skillpilot.com"
echo "   Password: admin123"
echo ""


#!/bin/bash

echo "🔧 Fixing CORS Settings"
echo "======================"
echo ""

echo "1️⃣ Updating CORS in .env..."
sed -i 's|CORS_ORIGINS=.*|CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://localhost,http://127.0.0.1,*|' .env
grep CORS .env

echo ""
echo "2️⃣ Restarting backend to apply changes..."
sudo docker-compose restart backend

echo ""
echo "3️⃣ Waiting for backend to start..."
sleep 8

echo ""
echo "4️⃣ Testing backend health..."
curl -s http://localhost:8000/health | jq . 2>/dev/null || curl -s http://localhost:8000/health

echo ""
echo "5️⃣ Testing CORS with OPTIONS request..."
curl -X OPTIONS http://localhost:8000/api/auth/login \
  -H "Origin: http://localhost" \
  -H "Access-Control-Request-Method: POST" \
  -v 2>&1 | grep -i "access-control"

echo ""
echo "✅ CORS fix applied!"
echo ""
echo "🌐 Now try logging in at: http://localhost"
echo ""


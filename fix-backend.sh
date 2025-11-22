#!/bin/bash

echo "🔧 Fixing Backend (Reusing Existing Libraries)"
echo "=============================================="
echo ""

echo "⏹️  Stopping backend..."
sudo docker-compose stop backend

echo ""
echo "🗑️  Removing old backend container (but keeping downloaded libraries)..."
sudo docker rm -f skillpilot_backend

echo ""
echo "🔨 Installing only the missing/updated packages inside container..."
sudo docker-compose run --rm backend pip install --upgrade openai==1.52.0 httpx==0.27.0

echo ""
echo "🚀 Starting backend..."
sudo docker-compose up -d backend

echo ""
echo "⏳ Waiting for backend to start..."
sleep 10

echo ""
echo "📊 Checking status..."
sudo docker-compose ps

echo ""
echo "📋 Backend logs:"
sudo docker-compose logs --tail=30 backend

echo ""
echo "✅ Done!"
echo ""
echo "🔍 Test: curl http://localhost:8000/health"
echo ""


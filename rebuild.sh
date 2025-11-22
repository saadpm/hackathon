#!/bin/bash

echo "🔧 Rebuilding SkillPilot AI Backend..."
echo "======================================"
echo ""

echo "⏹️  Stopping backend..."
sudo docker-compose stop backend

echo ""
echo "🔨 Rebuilding backend with updated dependencies..."
sudo docker-compose build --no-cache backend

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
echo "📋 Recent backend logs:"
sudo docker-compose logs --tail=20 backend

echo ""
echo "✅ Rebuild complete!"
echo ""
echo "🔍 Test the backend:"
echo "   curl http://localhost:8000/health"
echo ""


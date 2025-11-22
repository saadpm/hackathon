#!/bin/bash

echo "🎯 SkillPilot AI - Quick Start (Lightweight Version)"
echo "===================================================="
echo ""

echo "⏹️  Stopping all containers..."
sudo docker-compose down

echo ""
echo "🧹 Cleaning up..."
sudo docker system prune -f

echo ""
echo "🚀 Building with lightweight dependencies (no PyTorch)..."
sudo docker-compose build --no-cache backend

echo ""
echo "🎬 Starting all services..."
sudo docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 15

echo ""
echo "📊 Checking status..."
sudo docker-compose ps

echo ""
echo "✅ SkillPilot AI is running!"
echo ""
echo "📍 Access the application:"
echo "   Frontend: http://localhost"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔑 Demo Credentials:"
echo "   OD Manager: admin@skillpilot.com / admin123"
echo "   Employee: john.doe@skillpilot.com / admin123"
echo ""
echo "💡 This version uses TF-IDF instead of PyTorch (much faster!)"
echo ""


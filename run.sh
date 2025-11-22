#!/bin/bash

echo "🎯 SkillPilot AI - Starting Application"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from example..."
    cp env.example .env
    echo "✅ Created .env file. Please update OPENAI_API_KEY and OPENAI_BASE_URL"
    echo ""
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🐳 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "✅ SkillPilot AI is now running!"
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
echo "📊 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop the application:"
echo "   docker-compose down"
echo ""


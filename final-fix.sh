#!/bin/bash

echo "🔧 Complete Backend Fix - Rebuild Everything"
echo "============================================="
echo ""

echo "1️⃣ Stopping all containers..."
sudo docker-compose down

echo ""
echo "2️⃣ Rebuilding backend with correct dependencies..."
sudo docker-compose build --no-cache backend

echo ""
echo "3️⃣ Starting all services..."
sudo docker-compose up -d

echo ""
echo "4️⃣ Waiting for services to start..."
sleep 20

echo ""
echo "5️⃣ Checking bcrypt version in container..."
sudo docker-compose exec backend pip list | grep bcrypt

echo ""
echo "6️⃣ Resetting users with fresh password hashes..."
sudo docker-compose exec -T mysql mysql -u skillpilot -pskillpilot123 skillpilot_db <<EOF
SET FOREIGN_KEY_CHECKS = 0;
DELETE FROM employee_skills;
DELETE FROM assessment_results;
DELETE FROM learning_roadmaps;
DELETE FROM users;

INSERT INTO users (id, name, email, password_hash, role, job_title_id, years_of_experience) VALUES
(1, 'Admin User', 'admin@skillpilot.com', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYNq8QQ8pKS', 'OD_MANAGER', NULL, 10),
(2, 'John Doe', 'john.doe@skillpilot.com', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYNq8QQ8pKS', 'EMPLOYEE', 1, 1.5);

SET FOREIGN_KEY_CHECKS = 1;
SELECT id, name, email, role FROM users;
EOF

echo ""
echo "7️⃣ Testing login API..."
sleep 2
RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@skillpilot.com","password":"admin123"}')

echo ""
if echo "$RESPONSE" | grep -q "access_token"; then
    echo "✅ SUCCESS! Login is working!"
    echo "   Access token received"
else
    echo "❌ Login still failing:"
    echo "   $RESPONSE"
    echo ""
    echo "Checking backend logs for errors..."
    sudo docker-compose logs backend | tail -10
fi

echo ""
echo "8️⃣ Checking all services..."
sudo docker-compose ps

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Try logging in at: http://localhost"
echo "   Email: admin@skillpilot.com"
echo "   Password: admin123"
echo ""


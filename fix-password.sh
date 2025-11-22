#!/bin/bash

echo "🔑 Generating Fresh Password Hash in Container"
echo "=============================================="
echo ""

echo "1️⃣ Generating password hash for 'admin123' using container's bcrypt..."
HASH=$(sudo docker-compose exec -T backend python3 -c "
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
print(pwd_context.hash('admin123'))
" 2>/dev/null | tr -d '\r')

echo "Generated hash: $HASH"
echo ""

echo "2️⃣ Updating users in database with new hash..."
sudo docker-compose exec -T mysql mysql -u skillpilot -pskillpilot123 skillpilot_db <<EOF
SET FOREIGN_KEY_CHECKS = 0;
DELETE FROM employee_skills;
DELETE FROM assessment_results;
DELETE FROM learning_roadmaps;
DELETE FROM users;

INSERT INTO users (id, name, email, password_hash, role, job_title_id, years_of_experience) VALUES
(1, 'Admin User', 'admin@skillpilot.com', '$HASH', 'OD_MANAGER', NULL, 10),
(2, 'John Doe', 'john.doe@skillpilot.com', '$HASH', 'EMPLOYEE', 1, 1.5);

SET FOREIGN_KEY_CHECKS = 1;
SELECT id, name, email, role FROM users;
EOF

echo ""
echo "3️⃣ Testing login..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@skillpilot.com","password":"admin123"}')

echo ""
if echo "$RESPONSE" | grep -q "access_token"; then
    echo "✅ SUCCESS! Login is working!"
    echo ""
    echo "Response preview:"
    echo "$RESPONSE" | head -c 200
    echo "..."
else
    echo "❌ Login failed:"
    echo "$RESPONSE"
    echo ""
    echo "Checking backend logs..."
    sudo docker-compose logs backend | grep -A5 "POST /api/auth/login" | tail -20
fi

echo ""
echo ""
echo "🌐 Try logging in at: http://localhost"
echo "   Email: admin@skillpilot.com"
echo "   Password: admin123"
echo ""


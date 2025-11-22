-- SkillPilot AI Database Schema

-- Drop tables if they exist
DROP TABLE IF EXISTS learning_roadmaps;
DROP TABLE IF EXISTS assessment_results;
DROP TABLE IF EXISTS quiz_questions;
DROP TABLE IF EXISTS employee_skills;
DROP TABLE IF EXISTS job_descriptions;
DROP TABLE IF EXISTS job_titles;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('OD_MANAGER', 'EMPLOYEE') NOT NULL DEFAULT 'EMPLOYEE',
    job_title_id INT,
    years_of_experience DECIMAL(3,1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job Titles table
CREATE TABLE job_titles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    level INT NOT NULL COMMENT 'Career level: 1=Junior, 2=Mid, 3=Senior, 4=Lead, etc.',
    next_level_job_id INT COMMENT 'ID of next career level job',
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_title_level (title, level),
    FOREIGN KEY (next_level_job_id) REFERENCES job_titles(id) ON DELETE SET NULL,
    INDEX idx_level (level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job Descriptions table
CREATE TABLE job_descriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_title_id INT NOT NULL,
    required_skills JSON NOT NULL COMMENT 'Array of required skills with proficiency levels',
    required_tools JSON NOT NULL COMMENT 'Array of required tools/technologies',
    required_years_of_experience DECIMAL(3,1) NOT NULL,
    competency_weightage JSON COMMENT 'Weightage for different skill categories',
    expected_proficiency_levels JSON COMMENT 'Expected proficiency for each skill',
    preferred_skills JSON COMMENT 'Optional/preferred skills',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (job_title_id) REFERENCES job_titles(id) ON DELETE CASCADE,
    INDEX idx_job_title (job_title_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Employee Skills table
CREATE TABLE employee_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_name VARCHAR(255) NOT NULL,
    proficiency_level ENUM('beginner', 'intermediate', 'advanced', 'expert') NOT NULL,
    years_of_experience DECIMAL(3,1) DEFAULT 0,
    self_assessment_score INT CHECK (self_assessment_score BETWEEN 1 AND 10),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_skill (user_id, skill_name),
    INDEX idx_user (user_id),
    INDEX idx_skill (skill_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Quiz Questions table
CREATE TABLE quiz_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_title_id INT NOT NULL,
    skill_name VARCHAR(255) NOT NULL,
    question_text TEXT NOT NULL,
    options JSON NOT NULL COMMENT 'Array of answer options',
    correct_answer VARCHAR(255) NOT NULL,
    difficulty_level ENUM('beginner', 'intermediate', 'advanced', 'expert') NOT NULL,
    experience_level_years DECIMAL(3,1) COMMENT 'Target experience level',
    points INT DEFAULT 1,
    explanation TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT COMMENT 'OD Manager who created/approved',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (job_title_id) REFERENCES job_titles(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_job_skill (job_title_id, skill_name),
    INDEX idx_difficulty (difficulty_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Assessment Results table
CREATE TABLE assessment_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    quiz_question_id INT NOT NULL,
    selected_answer VARCHAR(255) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    points_earned INT DEFAULT 0,
    time_taken_seconds INT,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (quiz_question_id) REFERENCES quiz_questions(id) ON DELETE CASCADE,
    INDEX idx_user_quiz (user_id, quiz_question_id),
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Learning Roadmaps table
CREATE TABLE learning_roadmaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    job_title_id INT NOT NULL,
    skill_name VARCHAR(255) NOT NULL,
    current_level ENUM('beginner', 'intermediate', 'advanced', 'expert'),
    target_level ENUM('beginner', 'intermediate', 'advanced', 'expert') NOT NULL,
    gap_percentage DECIMAL(5,2),
    milestones JSON NOT NULL COMMENT 'Weekly/monthly learning milestones',
    course_recommendations JSON COMMENT 'Recommended courses with links',
    practice_tasks JSON COMMENT 'Tasks and projects to complete',
    estimated_completion_weeks INT,
    status ENUM('not_started', 'in_progress', 'completed', 'paused') DEFAULT 'not_started',
    progress_percentage DECIMAL(5,2) DEFAULT 0,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_title_id) REFERENCES job_titles(id) ON DELETE CASCADE,
    INDEX idx_user_status (user_id, status),
    INDEX idx_skill (skill_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Add foreign key to users table for job_title_id
ALTER TABLE users ADD FOREIGN KEY (job_title_id) REFERENCES job_titles(id) ON DELETE SET NULL;

-- Seed data: Create default OD Manager
INSERT INTO users (name, email, password_hash, role, years_of_experience) VALUES
('Admin User', 'admin@skillpilot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYNq8QQ8pKS', 'OD_MANAGER', 10);
-- Default password: admin123

-- Seed data: Job Titles with career progression
INSERT INTO job_titles (title, level, department) VALUES
('Junior MERN Developer', 1, 'Engineering'),
('MERN Developer', 2, 'Engineering'),
('Senior MERN Developer', 3, 'Engineering'),
('Lead MERN Developer', 4, 'Engineering'),
('Junior Python Developer', 1, 'Engineering'),
('Python Developer', 2, 'Engineering'),
('Senior Python Developer', 3, 'Engineering'),
('Junior DevOps Engineer', 1, 'Operations'),
('DevOps Engineer', 2, 'Operations'),
('Senior DevOps Engineer', 3, 'Operations');

-- Link career progression paths
UPDATE job_titles SET next_level_job_id = 2 WHERE id = 1;
UPDATE job_titles SET next_level_job_id = 3 WHERE id = 2;
UPDATE job_titles SET next_level_job_id = 4 WHERE id = 3;
UPDATE job_titles SET next_level_job_id = 6 WHERE id = 5;
UPDATE job_titles SET next_level_job_id = 7 WHERE id = 6;
UPDATE job_titles SET next_level_job_id = 9 WHERE id = 8;
UPDATE job_titles SET next_level_job_id = 10 WHERE id = 9;

-- Seed data: Job Descriptions
INSERT INTO job_descriptions (job_title_id, required_skills, required_tools, required_years_of_experience, competency_weightage, expected_proficiency_levels, preferred_skills, description) VALUES
(1, 
 '["JavaScript", "React", "Node.js", "Express", "MongoDB", "HTML", "CSS", "Git"]',
 '["VS Code", "Postman", "MongoDB Compass", "Git"]',
 0.5,
 '{"technical": 0.6, "problem_solving": 0.2, "communication": 0.2}',
 '{"JavaScript": "intermediate", "React": "intermediate", "Node.js": "beginner", "Express": "beginner", "MongoDB": "beginner"}',
 '["TypeScript", "Redux", "Jest", "Docker"]',
 'Entry-level MERN stack developer responsible for building web applications under supervision.'
),
(2,
 '["JavaScript", "TypeScript", "React", "Node.js", "Express", "MongoDB", "RESTful APIs", "Git", "Testing"]',
 '["VS Code", "Postman", "MongoDB Compass", "Git", "Jest", "Docker"]',
 2.0,
 '{"technical": 0.7, "problem_solving": 0.2, "communication": 0.1}',
 '{"JavaScript": "advanced", "TypeScript": "intermediate", "React": "advanced", "Node.js": "intermediate", "Express": "intermediate", "MongoDB": "intermediate"}',
 '["Redux", "GraphQL", "AWS", "CI/CD", "Microservices"]',
 'Mid-level MERN developer capable of independently building full-stack applications.'
),
(3,
 '["JavaScript", "TypeScript", "React", "Node.js", "Express", "MongoDB", "System Design", "Architecture", "Mentoring", "Code Review"]',
 '["VS Code", "Postman", "Git", "Jest", "Docker", "Kubernetes", "AWS/GCP"]',
 5.0,
 '{"technical": 0.5, "problem_solving": 0.2, "leadership": 0.2, "communication": 0.1}',
 '{"JavaScript": "expert", "TypeScript": "advanced", "React": "expert", "Node.js": "advanced", "System Design": "advanced"}',
 '["GraphQL", "Microservices", "Redis", "Message Queues", "Performance Optimization"]',
 'Senior MERN developer with strong architectural skills and mentoring capabilities.'
);

-- Add sample employee
INSERT INTO users (name, email, password_hash, role, job_title_id, years_of_experience) VALUES
('John Doe', 'john.doe@skillpilot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYNq8QQ8pKS', 'EMPLOYEE', 1, 1.5);
-- Default password: admin123


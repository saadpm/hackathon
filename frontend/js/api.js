// API Service Layer

const API = {
    // Auth
    async login(email, password) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        return await response.json();
    },

    async register(name, email, password, role) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password, role })
        });
        return await response.json();
    },

    // Job Titles
    async getJobTitles() {
        const response = await fetch(`${CONFIG.API_BASE_URL}/job/titles`, {
            headers: getAuthHeaders()
        });
        return await response.json();
    },

    async createJobTitle(data) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/job/titles`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        return await response.json();
    },

    // Job Descriptions
    async getJobDescriptions(jobTitleId = null) {
        const url = jobTitleId 
            ? `${CONFIG.API_BASE_URL}/job/descriptions?job_title_id=${jobTitleId}`
            : `${CONFIG.API_BASE_URL}/job/descriptions`;
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        return await response.json();
    },

    async createJobDescription(data) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/job/descriptions`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        return await response.json();
    },

    // Skills
    async submitSkills(skills) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/assessment/submit-skills`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ skills })
        });
        return await response.json();
    },

    async getMySkills() {
        const response = await fetch(`${CONFIG.API_BASE_URL}/assessment/my-skills`, {
            headers: getAuthHeaders()
        });
        return await response.json();
    },

    // Gap Analysis
    async getGapAnalysis() {
        const response = await fetch(`${CONFIG.API_BASE_URL}/assessment/gap-analysis`, {
            headers: getAuthHeaders()
        });
        return await response.json();
    },

    // Quiz
    async generateQuiz(data) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/quiz/generate`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        return await response.json();
    },

    async getQuizQuestions(jobTitleId = null, skillName = null) {
        let url = `${CONFIG.API_BASE_URL}/quiz/questions?`;
        if (jobTitleId) url += `job_title_id=${jobTitleId}&`;
        if (skillName) url += `skill_name=${skillName}`;
        
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        return await response.json();
    },

    async submitQuiz(answers) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/quiz/submit`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ answers })
        });
        return await response.json();
    },

    async getMyResults() {
        const response = await fetch(`${CONFIG.API_BASE_URL}/quiz/results`, {
            headers: getAuthHeaders()
        });
        return await response.json();
    },

    // Roadmap
    async generateRoadmap(skillName, targetLevel) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/roadmap/generate`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ skill_name: skillName, target_level: targetLevel })
        });
        return await response.json();
    },

    async getMyRoadmaps() {
        const response = await fetch(`${CONFIG.API_BASE_URL}/roadmap/my-roadmaps`, {
            headers: getAuthHeaders()
        });
        return await response.json();
    },

    async updateRoadmapProgress(roadmapId, progressPercentage) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/roadmap/roadmaps/${roadmapId}/progress?progress_percentage=${progressPercentage}`, {
            method: 'PUT',
            headers: getAuthHeaders()
        });
        return await response.json();
    },

    // Reports (OD Manager)
    async getEmployees() {
        const response = await fetch(`${CONFIG.API_BASE_URL}/reports/employees`, {
            headers: getAuthHeaders()
        });
        
        if (response.status === 401) {
            console.error('Unauthorized - token may be invalid');
            logout();
            throw new Error('Unauthorized');
        }
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    },

    async getEmployeeReport(employeeId) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/reports/employee/${employeeId}`, {
            headers: getAuthHeaders()
        });
        return await response.json();
    },

    async getCareerProgression(employeeId) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/reports/career-progression/${employeeId}`, {
            headers: getAuthHeaders()
        });
        return await response.json();
    }
};


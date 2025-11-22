// Dashboard logic

if (!requireAuth()) {
    throw new Error('Not authenticated');
}

const user = getUser();
const isODManager = user.role === 'OD_MANAGER';
const isEmployee = user.role === 'EMPLOYEE';

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    displayUserInfo();
    loadDashboard();
});

function initNavigation() {
    const navMenu = document.getElementById('navMenu');
    
    let menuItems = [];
    
    if (isODManager) {
        menuItems = [
            { name: 'Dashboard', page: 'dashboard', icon: '📊' },
            { name: 'Employees', page: 'employees', icon: '👥' },
            { name: 'Job Titles', page: 'job-titles', icon: '💼' },
            { name: 'Job Descriptions', page: 'job-descriptions', icon: '📝' },
            { name: 'Generate Quiz', page: 'generate-quiz', icon: '❓' }
        ];
    } else if (isEmployee) {
        menuItems = [
            { name: 'Dashboard', page: 'dashboard', icon: '📊' },
            { name: 'My Skills', page: 'my-skills', icon: '⭐' },
            { name: 'Gap Analysis', page: 'gap-analysis', icon: '📈' },
            { name: 'Take Quiz', page: 'take-quiz', icon: '✍️' },
            { name: 'Learning Roadmap', page: 'roadmap', icon: '🗺️' }
        ];
    }
    
    navMenu.innerHTML = menuItems.map(item => `
        <li>
            <a href="#" onclick="loadPage('${item.page}'); return false;">
                ${item.icon} ${item.name}
            </a>
        </li>
    `).join('');
}

function displayUserInfo() {
    document.getElementById('userName').textContent = user.name;
    const roleSpan = document.getElementById('userRole');
    roleSpan.textContent = user.role.replace('_', ' ');
    roleSpan.className = `badge badge-${isODManager ? 'manager' : 'employee'}`;
}

function loadPage(page) {
    const content = document.getElementById('mainContent');
    const pageTitle = document.getElementById('pageTitle');
    
    // Update active menu item
    document.querySelectorAll('.nav-menu a').forEach(a => a.classList.remove('active'));
    event.target.classList.add('active');
    
    switch(page) {
        case 'dashboard':
            pageTitle.textContent = 'Dashboard';
            if (isODManager) loadODManagerDashboard(content);
            else loadEmployeeDashboard(content);
            break;
        case 'employees':
            pageTitle.textContent = 'Employee Management';
            loadEmployeesPage(content);
            break;
        case 'job-titles':
            pageTitle.textContent = 'Job Titles';
            loadJobTitlesPage(content);
            break;
        case 'job-descriptions':
            pageTitle.textContent = 'Job Descriptions';
            loadJobDescriptionsPage(content);
            break;
        case 'generate-quiz':
            pageTitle.textContent = 'Generate Quiz';
            loadGenerateQuizPage(content);
            break;
        case 'my-skills':
            pageTitle.textContent = 'My Skills';
            loadMySkillsPage(content);
            break;
        case 'gap-analysis':
            pageTitle.textContent = 'Gap Analysis';
            loadGapAnalysisPage(content);
            break;
        case 'take-quiz':
            pageTitle.textContent = 'Take Assessment Quiz';
            loadTakeQuizPage(content);
            break;
        case 'roadmap':
            pageTitle.textContent = 'Learning Roadmap';
            loadRoadmapPage(content);
            break;
    }
}

function loadDashboard() {
    const content = document.getElementById('mainContent');
    if (isODManager) loadODManagerDashboard(content);
    else loadEmployeeDashboard(content);
}

// OD Manager Dashboard
async function loadODManagerDashboard(content) {
    content.innerHTML = '<div class="loading">Loading dashboard data</div>';
    
    try {
        const employees = await API.getEmployees();
        
        const totalEmployees = employees.length;
        const totalSkills = employees.reduce((sum, emp) => sum + emp.total_skills, 0);
        const activeRoadmaps = employees.reduce((sum, emp) => sum + emp.active_roadmaps, 0);
        
        content.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Total Employees</h3>
                    <div class="stat-value">${totalEmployees}</div>
                </div>
                <div class="stat-card">
                    <h3>Total Skills</h3>
                    <div class="stat-value">${totalSkills}</div>
                </div>
                <div class="stat-card">
                    <h3>Active Roadmaps</h3>
                    <div class="stat-value">${activeRoadmaps}</div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">Recent Employee Activity</div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Job Title</th>
                                <th>Skills</th>
                                <th>Assessments</th>
                                <th>Active Roadmaps</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${employees.map(emp => `
                                <tr>
                                    <td>${emp.name}</td>
                                    <td>${emp.job_title || 'Not assigned'}</td>
                                    <td>${emp.total_skills}</td>
                                    <td>${emp.total_assessments}</td>
                                    <td>${emp.active_roadmaps}</td>
                                    <td>
                                        <button class="btn btn-primary" onclick="viewEmployeeReport(${emp.id})">View Report</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    } catch (error) {
        content.innerHTML = '<div class="error-message show">Failed to load dashboard data</div>';
        console.error('Dashboard error:', error);
    }
}

// Employee Dashboard
async function loadEmployeeDashboard(content) {
    content.innerHTML = '<div class="loading">Loading your dashboard</div>';
    
    try {
        const [skills, roadmaps, results] = await Promise.all([
            API.getMySkills(),
            API.getMyRoadmaps(),
            API.getMyResults()
        ]);
        
        const activeRoadmaps = roadmaps.filter(r => r.status === 'in_progress').length;
        const completedRoadmaps = roadmaps.filter(r => r.status === 'completed').length;
        
        content.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>My Skills</h3>
                    <div class="stat-value">${skills.length}</div>
                </div>
                <div class="stat-card">
                    <h3>Active Roadmaps</h3>
                    <div class="stat-value">${activeRoadmaps}</div>
                </div>
                <div class="stat-card">
                    <h3>Completed Roadmaps</h3>
                    <div class="stat-value">${completedRoadmaps}</div>
                </div>
                <div class="stat-card">
                    <h3>Assessments Taken</h3>
                    <div class="stat-value">${results.length}</div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">Quick Actions</div>
                <div class="stats-grid">
                    <button class="btn btn-primary" onclick="loadPage('my-skills')">Update My Skills</button>
                    <button class="btn btn-primary" onclick="loadPage('gap-analysis')">View Gap Analysis</button>
                    <button class="btn btn-primary" onclick="loadPage('take-quiz')">Take Quiz</button>
                    <button class="btn btn-primary" onclick="loadPage('roadmap')">View Roadmap</button>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">My Skills Overview</div>
                <div class="skills-grid">
                    ${skills.map(skill => `
                        <div class="skill-item">
                            <h4>${skill.skill_name}</h4>
                            <div class="proficiency">${skill.proficiency_level} - ${skill.years_of_experience} years</div>
                        </div>
                    `).join('') || '<p class="text-muted">No skills added yet. Click "Update My Skills" to add your skills.</p>'}
                </div>
            </div>
        `;
    } catch (error) {
        content.innerHTML = '<div class="error-message show">Failed to load dashboard data</div>';
        console.error('Dashboard error:', error);
    }
}

// Additional page loaders will be added in separate files
// For brevity, placeholders below

async function loadEmployeesPage(content) {
    content.innerHTML = '<div class="loading">Loading employees</div>';
    try {
        const employees = await API.getEmployees();
        content.innerHTML = `
            <div class="card">
                <div class="card-header">All Employees</div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Job Title</th>
                                <th>Experience</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${employees.map(emp => `
                                <tr>
                                    <td>${emp.name}</td>
                                    <td>${emp.email}</td>
                                    <td>${emp.job_title || 'Not assigned'}</td>
                                    <td>${emp.years_of_experience} years</td>
                                    <td>
                                        <button class="btn btn-primary" onclick="viewEmployeeReport(${emp.id})">View Details</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    } catch (error) {
        content.innerHTML = '<div class="error-message show">Failed to load employees</div>';
    }
}

async function viewEmployeeReport(employeeId) {
    const content = document.getElementById('mainContent');
    const pageTitle = document.getElementById('pageTitle');
    pageTitle.textContent = 'Employee Report';
    
    content.innerHTML = '<div class="loading">Loading employee report</div>';
    
    try {
        const report = await API.getEmployeeReport(employeeId);
        
        content.innerHTML = `
            <div class="card">
                <div class="card-header">Employee Information</div>
                <p><strong>Name:</strong> ${report.user.name}</p>
                <p><strong>Email:</strong> ${report.user.email}</p>
                <p><strong>Job Title:</strong> ${report.user.job_title || 'Not assigned'}</p>
                <p><strong>Experience:</strong> ${report.user.years_of_experience} years</p>
            </div>
            
            <div class="card">
                <div class="card-header">Skills (${report.skills.length})</div>
                <div class="skills-grid">
                    ${report.skills.map(skill => `
                        <div class="skill-item">
                            <h4>${skill.skill_name}</h4>
                            <div class="proficiency">${skill.proficiency_level} - ${skill.years_of_experience} years</div>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            ${report.gap_analysis ? `
                <div class="card">
                    <div class="card-header">Gap Analysis</div>
                    <p><strong>Gap Percentage:</strong> ${report.gap_analysis.gap_percentage}%</p>
                    <p><strong>Missing Skills:</strong> ${report.gap_analysis.missing_skills.join(', ')}</p>
                    <p><strong>Priority Areas:</strong> ${report.gap_analysis.priority_areas.join(', ')}</p>
                </div>
            ` : ''}
            
            <button class="btn btn-secondary" onclick="loadPage('employees')">Back to Employees</button>
        `;
    } catch (error) {
        content.innerHTML = '<div class="error-message show">Failed to load employee report</div>';
    }
}

async function loadJobTitlesPage(content) {
    content.innerHTML = '<p class="text-muted">Job Titles management - Coming soon</p>';
}

async function loadJobDescriptionsPage(content) {
    content.innerHTML = '<p class="text-muted">Job Descriptions management - Coming soon</p>';
}

async function loadGenerateQuizPage(content) {
    content.innerHTML = '<p class="text-muted">Quiz generation - Coming soon</p>';
}

async function loadMySkillsPage(content) {
    content.innerHTML = '<p class="text-muted">Skills management - Coming soon</p>';
}

async function loadGapAnalysisPage(content) {
    content.innerHTML = '<p class="text-muted">Gap analysis - Coming soon</p>';
}

async function loadTakeQuizPage(content) {
    content.innerHTML = '<p class="text-muted">Quiz assessment - Coming soon</p>';
}

async function loadRoadmapPage(content) {
    content.innerHTML = '<p class="text-muted">Learning roadmap - Coming soon</p>';
}


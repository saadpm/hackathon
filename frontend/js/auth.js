// Authentication utilities

function setAuthToken(token) {
    localStorage.setItem(CONFIG.TOKEN_KEY, token);
}

function getAuthToken() {
    return localStorage.getItem(CONFIG.TOKEN_KEY);
}

function setUser(user) {
    localStorage.setItem(CONFIG.USER_KEY, JSON.stringify(user));
}

function getUser() {
    const userStr = localStorage.getItem(CONFIG.USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
}

function isAuthenticated() {
    return !!getAuthToken();
}

function logout() {
    localStorage.removeItem(CONFIG.TOKEN_KEY);
    localStorage.removeItem(CONFIG.USER_KEY);
    window.location.href = 'index.html';
}

function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

function getAuthHeaders() {
    const token = getAuthToken();
    console.log('Getting auth headers, token:', token ? 'EXISTS' : 'MISSING');
    
    if (!token) {
        console.error('No token found in localStorage!');
    }
    
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}


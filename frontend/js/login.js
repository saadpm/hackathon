// Login page logic

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('errorMessage');
    
    try {
        const data = await API.login(email, password);
        
        if (data.access_token) {
            setAuthToken(data.access_token);
            setUser(data.user);
            window.location.href = 'dashboard.html';
        } else {
            errorDiv.textContent = data.detail || 'Login failed';
            errorDiv.classList.add('show');
        }
    } catch (error) {
        errorDiv.textContent = 'An error occurred. Please try again.';
        errorDiv.classList.add('show');
        console.error('Login error:', error);
    }
});


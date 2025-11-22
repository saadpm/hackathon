// Login page logic

console.log('Login page loaded');

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('errorMessage');
    
    console.log('Login attempt for:', email);
    console.log('API URL:', CONFIG.API_BASE_URL);
    
    // Clear previous errors
    errorDiv.textContent = '';
    errorDiv.classList.remove('show');
    
    try {
        console.log('Calling API.login...');
        const data = await API.login(email, password);
        console.log('API response:', data);
        
        if (data.access_token) {
            console.log('Login successful!');
            setAuthToken(data.access_token);
            setUser(data.user);
            window.location.href = 'dashboard.html';
        } else {
            console.log('Login failed:', data);
            errorDiv.textContent = data.detail || 'Login failed';
            errorDiv.classList.add('show');
        }
    } catch (error) {
        console.error('Login error:', error);
        errorDiv.textContent = 'Cannot connect to server. Please check if backend is running.';
        errorDiv.classList.add('show');
    }
});


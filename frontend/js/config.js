// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api'
    : '/api';

const CONFIG = {
    API_BASE_URL,
    TOKEN_KEY: 'skillpilot_token',
    USER_KEY: 'skillpilot_user'
};


import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Resume API calls
export const resumeAPI = {
  upload: (file: File) => {
    const formData = new FormData();
    formData.append('resume', file);
    return api.post('/resumes/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  list: () => api.get('/resumes/'),
  
  get: (id: string) => api.get(`/resumes/${id}/`),
  
  delete: (id: string) => api.delete(`/resumes/${id}/`),
};

// AI Services API calls
export const aiAPI = {
  analyzeResume: (data: {
    resume_text: string;
    analysis_type?: string;
    target_role?: string;
  }) => api.post('/ai/analyze-resume/', data),
  
  matchJobs: (data: {
    resume_text: string;
    preferences?: any;
    use_perplexity?: boolean;
    limit?: number;
  }) => api.post('/ai/match-jobs/', data),
  
  getCareerAdvice: (data: {
    resume_text: string;
    career_goals?: string;
    current_challenges?: string;
    preferred_industries?: string[];
  }) => api.post('/ai/career-advice/', data),
  
  researchMarket: (data: {
    industry: string;
    location?: string;
    role?: string;
    timeframe?: string;
  }) => api.post('/ai/research-market/', data),
  
  researchCompany: (data: {
    company_name: string;
    detailed?: boolean;
  }) => api.post('/ai/research-company/', data),
  
  collectLinkedInJobs: (data: {
    queries: string[];
    locations: string[];
    limit?: number;
  }) => api.post('/ai/collect-linkedin-jobs/', data),
  
  getStatus: () => api.get('/ai/status/'),
};

// Jobs API calls
export const jobsAPI = {
  list: (params?: {
    search?: string;
    location?: string;
    job_type?: string;
    experience_level?: string;
    page?: number;
  }) => api.get('/jobs/', { params }),
  
  get: (id: string) => api.get(`/jobs/${id}/`),
  
  apply: (jobId: string, data: {
    cover_letter?: string;
    resume_id?: string;
  }) => api.post(`/jobs/${jobId}/apply/`, data),
  
  getApplications: () => api.get('/jobs/applications/'),
};

// Authentication API calls (for future use)
export const authAPI = {
  login: (data: { email: string; password: string }) => 
    api.post('/auth/login/', data),
  
  register: (data: { 
    email: string; 
    password: string; 
    first_name: string; 
    last_name: string; 
  }) => api.post('/auth/register/', data),
  
  logout: () => api.post('/auth/logout/'),
  
  getProfile: () => api.get('/auth/profile/'),
  
  updateProfile: (data: any) => api.patch('/auth/profile/', data),
};

// Request/Response interceptors for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      // Redirect to login page
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

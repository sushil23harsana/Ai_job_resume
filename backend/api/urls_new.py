from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Main API endpoints
    path('', views.api_status, name='api_status'),
    path('status/', views.api_status, name='api_status'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('upload/', views.upload_resume, name='upload_resume_alt'),
    path('analyze-resume/', views.analyze_resume, name='analyze_resume'),
    path('search-jobs/', views.search_jobs, name='search_jobs'),
    
    # Resume endpoints (matching frontend expectations)
    path('resumes/upload/', views.upload_resume, name='resumes_upload'),
    path('resumes/analyze/', views.analyze_resume, name='resumes_analyze'),
    
    # AI Service endpoints
    path('ai/analyze-resume/', views.ai_analyze_resume, name='ai_analyze_resume'),
    path('ai/match-jobs/', views.ai_match_jobs, name='ai_match_jobs'),
    path('ai/career-advice/', views.ai_career_advice, name='ai_career_advice'),
    path('ai/research-market/', views.ai_research_market, name='ai_research_market'),
    path('ai/research-company/', views.ai_research_company, name='ai_research_company'),
    path('ai/collect-linkedin-jobs/', views.ai_collect_linkedin_jobs, name='ai_collect_linkedin_jobs'),
    path('ai/status/', views.ai_status, name='ai_status'),
]

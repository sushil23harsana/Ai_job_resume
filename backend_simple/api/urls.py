from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.api_status, name='api_status'),
    path('status/', views.api_status, name='api_status'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('analyze-resume/', views.analyze_resume, name='analyze_resume'),
    path('search-jobs/', views.search_jobs, name='search_jobs'),
]

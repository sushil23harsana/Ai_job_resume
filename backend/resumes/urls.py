from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'', views.ResumeViewSet, basename='resume')

app_name = 'resumes'

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    # Resume upload and management
    path('upload/', views.ResumeUploadView.as_view(), name='upload'),
    path('bulk-upload/', views.BulkResumeUploadView.as_view(), name='bulk_upload'),
    
    # Resume processing
    path('<uuid:resume_id>/process/', views.ProcessResumeView.as_view(), name='process'),
    path('<uuid:resume_id>/reprocess/', views.ReprocessResumeView.as_view(), name='reprocess'),
    path('<uuid:resume_id>/status/', views.ResumeProcessingStatusView.as_view(), name='processing_status'),
    
    # Resume data access
    path('<uuid:resume_id>/raw-text/', views.ResumeRawTextView.as_view(), name='raw_text'),
    path('<uuid:resume_id>/parsed-data/', views.ParsedDataView.as_view(), name='parsed_data'),
    path('<uuid:resume_id>/personal-info/', views.PersonalInfoView.as_view(), name='personal_info'),
    path('<uuid:resume_id>/experience/', views.WorkExperienceView.as_view(), name='work_experience'),
    path('<uuid:resume_id>/education/', views.EducationView.as_view(), name='education'),
    path('<uuid:resume_id>/skills/', views.SkillsView.as_view(), name='skills'),
    path('<uuid:resume_id>/projects/', views.ProjectsView.as_view(), name='projects'),
    path('<uuid:resume_id>/certifications/', views.CertificationsView.as_view(), name='certifications'),
    
    # AI Analysis
    path('<uuid:resume_id>/ai-analysis/', views.AIAnalysisView.as_view(), name='ai_analysis'),
    path('<uuid:resume_id>/analyze/', views.AnalyzeResumeView.as_view(), name='analyze'),
    path('<uuid:resume_id>/suggestions/', views.ImprovementSuggestionsView.as_view(), name='suggestions'),
    path('<uuid:resume_id>/optimization/', views.ResumeOptimizationView.as_view(), name='optimization'),
    
    # Resume comparison and analytics
    path('compare/', views.CompareResumesView.as_view(), name='compare'),
    path('analytics/', views.ResumeAnalyticsView.as_view(), name='analytics'),
    path('market-analysis/', views.MarketAnalysisView.as_view(), name='market_analysis'),
    
    # File operations
    path('<uuid:resume_id>/download/', views.DownloadResumeView.as_view(), name='download'),
    path('<uuid:resume_id>/preview/', views.PreviewResumeView.as_view(), name='preview'),
    
    # Include router URLs
    path('', include(router.urls)),
]

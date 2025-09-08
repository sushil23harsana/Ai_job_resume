from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from api import views as api_views

def api_status(request):
    return JsonResponse({
        'status': 'success',
        'message': 'Job Platform Backend API is running',
        'version': '1.0.0'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_status, name='api_status'),
    path('api/', include('api.urls')),
    # Add resume endpoints that frontend expects
    path('api/resumes/upload/', api_views.upload_resume, name='resumes_upload'),
    path('api/resumes/analyze/', api_views.analyze_resume, name='resumes_analyze'),
]

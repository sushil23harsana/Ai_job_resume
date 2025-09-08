from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

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
]

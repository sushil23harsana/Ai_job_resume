from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

class ResumeViewSet(viewsets.ViewSet):
    """
    Basic Resume ViewSet - placeholder for now
    """
    
    def list(self, request):
        return Response({'message': 'Resume API is working'})
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        return Response({'message': 'Resume upload endpoint - coming soon'})
    
    @action(detail=False, methods=['post'])
    def analyze(self, request):
        return Response({'message': 'Resume analysis endpoint - coming soon'})

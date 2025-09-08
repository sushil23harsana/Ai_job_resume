from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

class JobViewSet(viewsets.ViewSet):
    """Basic Job ViewSet - placeholder for now"""
    def list(self, request):
        return Response({'message': 'Jobs API is working'})

class CompanyViewSet(viewsets.ViewSet):
    """Basic Company ViewSet - placeholder for now"""
    def list(self, request):
        return Response({'message': 'Companies API is working'})

class JobCategoryViewSet(viewsets.ViewSet):
    """Basic JobCategory ViewSet - placeholder for now"""
    def list(self, request):
        return Response({'message': 'Job Categories API is working'})

class SavedJobViewSet(viewsets.ViewSet):
    """Basic SavedJob ViewSet - placeholder for now"""
    def list(self, request):
        return Response({'message': 'Saved Jobs API is working'})

class JobApplicationViewSet(viewsets.ViewSet):
    """Basic JobApplication ViewSet - placeholder for now"""
    def list(self, request):
        return Response({'message': 'Job Applications API is working'})

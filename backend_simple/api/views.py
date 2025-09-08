from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
from decouple import config
import json

# Configure Gemini API
try:
    genai.configure(api_key=config('GOOGLE_GEMINI_API_KEY', default=''))
except:
    pass  # Handle missing API key gracefully

@api_view(['GET'])
def api_status(request):
    """API status endpoint"""
    return Response({
        'status': 'success',
        'message': 'Job Platform API is running',
        'version': '1.0.0'
    })

@api_view(['POST'])
def upload_resume(request):
    """Simple resume upload endpoint"""
    if request.FILES.get('resume'):
        file = request.FILES['resume']
        return Response({
            'status': 'success',
            'message': f'Resume {file.name} uploaded successfully',
            'filename': file.name,
            'size': file.size
        })
    else:
        return Response({
            'status': 'error',
            'message': 'No resume file provided'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def analyze_resume(request):
    """Analyze resume with Gemini AI"""
    try:
        resume_text = request.data.get('resume_text', '')
        if not resume_text:
            return Response({
                'status': 'error',
                'message': 'No resume text provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use Gemini to analyze the resume
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Please analyze this resume and provide:
        1. Key skills identified
        2. Experience level
        3. Suggested job roles
        4. Areas for improvement
        
        Resume text: {resume_text}
        
        Please respond in JSON format.
        """
        
        response = model.generate_content(prompt)
        
        return Response({
            'status': 'success',
            'message': 'Resume analyzed successfully',
            'analysis': response.text
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Analysis failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def search_jobs(request):
    """Simple job search endpoint"""
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    
    # Placeholder job data
    jobs = [
        {
            'id': 1,
            'title': 'Software Engineer',
            'company': 'Tech Corp',
            'location': 'San Francisco, CA',
            'salary': '$100,000 - $150,000',
            'description': 'Looking for a skilled software engineer...'
        },
        {
            'id': 2,
            'title': 'Data Scientist',
            'company': 'Data Inc',
            'location': 'New York, NY',
            'salary': '$120,000 - $180,000',
            'description': 'Join our data science team...'
        }
    ]
    
    # Simple filtering based on query
    if query:
        jobs = [job for job in jobs if query.lower() in job['title'].lower()]
    
    return Response({
        'status': 'success',
        'jobs': jobs,
        'total': len(jobs)
    })

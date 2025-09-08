from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
from decouple import config
import json
import requests

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
    """Resume upload endpoint with text extraction"""
    try:
        if not request.FILES.get('resume'):
            return Response({
                'status': 'error',
                'message': 'No resume file provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['resume']
        file_name = file.name.lower()
        
        # Extract text based on file type
        text_content = ""
        
        try:
            if file_name.endswith('.pdf'):
                # Handle PDF files
                import PyPDF2
                import io
                
                pdf_file = io.BytesIO(file.read())
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
                    
            elif file_name.endswith(('.doc', '.docx')):
                # Handle Word documents
                import docx
                import io
                
                doc_file = io.BytesIO(file.read())
                doc = docx.Document(doc_file)
                
                for paragraph in doc.paragraphs:
                    text_content += paragraph.text + "\n"
                    
            else:
                return Response({
                    'status': 'error',
                    'message': 'Unsupported file format. Please upload PDF, DOC, or DOCX files.'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as extraction_error:
            return Response({
                'status': 'error',
                'message': f'Failed to extract text from file: {str(extraction_error)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not text_content.strip():
            return Response({
                'status': 'error',
                'message': 'No text content found in the uploaded file'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'status': 'success',
            'message': f'Resume {file.name} uploaded and processed successfully',
            'filename': file.name,
            'size': file.size,
            'text_content': text_content.strip(),
            'word_count': len(text_content.split())
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Upload failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        model = genai.GenerativeModel('gemini-1.5-flash')
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

# AI Service Endpoints
@api_view(['POST'])
def ai_analyze_resume(request):
    """AI Resume Analysis endpoint"""
    try:
        resume_text = request.data.get('resume_text', '')
        analysis_type = request.data.get('analysis_type', 'comprehensive')
        target_role = request.data.get('target_role', '')
        
        if not resume_text:
            return Response({
                'status': 'error',
                'message': 'No resume text provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Analyze this resume for: {analysis_type}
        Target role: {target_role}
        
        Resume: {resume_text}
        
        Provide detailed analysis including:
        1. Skills assessment
        2. Experience evaluation
        3. Strengths and weaknesses
        4. Improvement suggestions
        5. Job match score (1-10)
        
        Return in JSON format.
        """
        
        response = model.generate_content(prompt)
        
        return Response({
            'status': 'success',
            'analysis': {
                'resume_text': resume_text,
                'analysis_type': analysis_type,
                'target_role': target_role,
                'ai_analysis': response.text,
                'score': 8.5  # Placeholder score
            }
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'AI analysis failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def ai_match_jobs(request):
    """AI Job Matching endpoint"""
    try:
        resume_text = request.data.get('resume_text', '')
        preferences = request.data.get('preferences', {})
        use_perplexity = request.data.get('use_perplexity', False)
        limit = request.data.get('limit', 10)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Based on this resume, suggest matching jobs:
        Resume: {resume_text}
        Preferences: {preferences}
        
        Provide {limit} job suggestions with:
        1. Job title
        2. Company type
        3. Required skills
        4. Match percentage
        5. Salary range
        
        Return in JSON format.
        """
        
        response = model.generate_content(prompt)
        
        return Response({
            'status': 'success',
            'matches': {
                'total_found': limit,
                'jobs': response.text,
                'use_perplexity': use_perplexity
            }
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Job matching failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def ai_career_advice(request):
    """AI Career Advice endpoint"""
    try:
        resume_text = request.data.get('resume_text', '')
        career_goals = request.data.get('career_goals', '')
        current_challenges = request.data.get('current_challenges', '')
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Provide career advice based on:
        Resume: {resume_text}
        Career Goals: {career_goals}
        Challenges: {current_challenges}
        
        Include:
        1. Career path recommendations
        2. Skill development suggestions
        3. Industry insights
        4. Next steps
        
        Return in JSON format.
        """
        
        response = model.generate_content(prompt)
        
        return Response({
            'status': 'success',
            'advice': response.text
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Career advice failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def ai_research_market(request):
    """AI Market Research endpoint"""
    try:
        industry = request.data.get('industry', '')
        location = request.data.get('location', '')
        role = request.data.get('role', '')
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Research the job market for:
        Industry: {industry}
        Location: {location}
        Role: {role}
        
        Provide:
        1. Market trends
        2. Salary ranges
        3. In-demand skills
        4. Growth prospects
        
        Return in JSON format.
        """
        
        response = model.generate_content(prompt)
        
        return Response({
            'status': 'success',
            'research': response.text
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Market research failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def ai_research_company(request):
    """AI Company Research endpoint"""
    try:
        company_name = request.data.get('company_name', '')
        detailed = request.data.get('detailed', False)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Research company: {company_name}
        Detailed analysis: {detailed}
        
        Provide:
        1. Company overview
        2. Culture and values
        3. Recent news
        4. Career opportunities
        5. Interview tips
        
        Return in JSON format.
        """
        
        response = model.generate_content(prompt)
        
        return Response({
            'status': 'success',
            'company_research': response.text
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Company research failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def ai_collect_linkedin_jobs(request):
    """AI LinkedIn Job Collection endpoint"""
    try:
        queries = request.data.get('queries', [])
        locations = request.data.get('locations', [])
        limit = request.data.get('limit', 50)
        
        # Use Perplexity API if available
        perplexity_api_key = config('PERPLEXITY_API_KEY', default='')
        
        if perplexity_api_key and perplexity_api_key != 'your-perplexity-api-key-here':
            try:
                # Call Perplexity API for job search
                perplexity_url = "https://api.perplexity.ai/chat/completions"
                headers = {
                    "Authorization": f"Bearer {perplexity_api_key}",
                    "Content-Type": "application/json"
                }
                
                prompt = f"""
                Find LinkedIn job postings for:
                Queries: {', '.join(queries)}
                Locations: {', '.join(locations)}
                Limit: {limit}
                
                Return job titles, companies, locations, and LinkedIn URLs.
                """
                
                data = {
                    "model": "llama-3.1-sonar-small-128k-online",
                    "messages": [{"role": "user", "content": prompt}]
                }
                
                response = requests.post(perplexity_url, headers=headers, json=data, timeout=30)
                perplexity_result = response.json()
                
                return Response({
                    'status': 'success',
                    'source': 'perplexity',
                    'jobs': perplexity_result.get('choices', [{}])[0].get('message', {}).get('content', '')
                })
                
            except Exception as perplexity_error:
                # Fall back to Gemini if Perplexity fails
                pass
        
        # Fallback to Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Help find LinkedIn job opportunities for:
        Search queries: {', '.join(queries)}
        Locations: {', '.join(locations)}
        Limit: {limit}
        
        Suggest job search strategies and provide sample job listings that might be found.
        Return in JSON format.
        """
        
        response = model.generate_content(prompt)
        
        return Response({
            'status': 'success',
            'source': 'gemini',
            'jobs': response.text,
            'note': 'This is AI-generated job search guidance. For actual LinkedIn jobs, integration with LinkedIn API would be required.'
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'LinkedIn job collection failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def ai_status(request):
    """AI Services status endpoint"""
    gemini_status = 'available' if config('GOOGLE_GEMINI_API_KEY', default='') else 'not configured'
    perplexity_status = 'available' if config('PERPLEXITY_API_KEY', default='') != 'your-perplexity-api-key-here' else 'not configured'
    
    return Response({
        'status': 'success',
        'ai_services': {
            'gemini': gemini_status,
            'perplexity': perplexity_status,
            'available_endpoints': [
                'analyze-resume',
                'match-jobs', 
                'career-advice',
                'research-market',
                'research-company',
                'collect-linkedin-jobs'
            ]
        }
    })

# Jobs API Endpoints
@api_view(['GET'])
def jobs_list(request):
    """List jobs with optional filtering"""
    search = request.GET.get('search', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')
    experience_level = request.GET.get('experience_level', '')
    page = request.GET.get('page', 1)
    
    # Sample job data - in a real app, this would come from a database
    sample_jobs = [
        {
            'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
            'title': 'Senior Software Engineer',
            'company': 'TechCorp Inc.',
            'location': 'San Francisco, CA',
            'job_type': 'Full-time',
            'experience_level': 'Senior',
            'salary_min': 150000,
            'salary_max': 200000,
            'description': 'We are looking for a senior software engineer to join our team...',
            'requirements': ['Python', 'Django', 'React', '5+ years experience'],
            'posted_date': '2025-09-01',
            'company_logo': 'https://example.com/logo1.png'
        },
        {
            'id': 'b2c3d4e5-f6g7-8901-bcde-f23456789012',
            'title': 'Data Scientist',
            'company': 'DataFlow Solutions',
            'location': 'New York, NY',
            'job_type': 'Full-time',
            'experience_level': 'Mid-level',
            'salary_min': 120000,
            'salary_max': 160000,
            'description': 'Join our data science team to work on cutting-edge ML projects...',
            'requirements': ['Python', 'Machine Learning', 'SQL', '3+ years experience'],
            'posted_date': '2025-09-03',
            'company_logo': 'https://example.com/logo2.png'
        },
        {
            'id': 'c3d4e5f6-g7h8-9012-cdef-345678901234',
            'title': 'Frontend Developer',
            'company': 'WebDesign Pro',
            'location': 'Austin, TX',
            'job_type': 'Remote',
            'experience_level': 'Junior',
            'salary_min': 80000,
            'salary_max': 110000,
            'description': 'Looking for a passionate frontend developer...',
            'requirements': ['React', 'TypeScript', 'CSS', '2+ years experience'],
            'posted_date': '2025-09-05',
            'company_logo': 'https://example.com/logo3.png'
        },
        {
            'id': 'd4e5f6g7-h8i9-0123-defg-456789012345',
            'title': 'DevOps Engineer',
            'company': 'CloudTech Systems',
            'location': 'Seattle, WA',
            'job_type': 'Full-time',
            'experience_level': 'Senior',
            'salary_min': 140000,
            'salary_max': 180000,
            'description': 'We need a DevOps engineer to manage our cloud infrastructure...',
            'requirements': ['AWS', 'Docker', 'Kubernetes', '4+ years experience'],
            'posted_date': '2025-09-07',
            'company_logo': 'https://example.com/logo4.png'
        },
        {
            'id': 'e5f6g7h8-i9j0-1234-efgh-567890123456',
            'title': 'Product Manager',
            'company': 'Innovation Labs',
            'location': 'Los Angeles, CA',
            'job_type': 'Full-time',
            'experience_level': 'Mid-level',
            'salary_min': 130000,
            'salary_max': 170000,
            'description': 'Lead product development for our next-generation platform...',
            'requirements': ['Product Management', 'Agile', 'Analytics', '3+ years experience'],
            'posted_date': '2025-09-06',
            'company_logo': 'https://example.com/logo5.png'
        }
    ]
    
    # Apply filters
    filtered_jobs = sample_jobs
    
    if search:
        filtered_jobs = [job for job in filtered_jobs 
                        if search.lower() in job['title'].lower() 
                        or search.lower() in job['company'].lower()
                        or any(search.lower() in req.lower() for req in job['requirements'])]
    
    if location:
        filtered_jobs = [job for job in filtered_jobs 
                        if location.lower() in job['location'].lower()]
    
    if job_type:
        filtered_jobs = [job for job in filtered_jobs 
                        if job_type.lower() == job['job_type'].lower()]
    
    if experience_level:
        filtered_jobs = [job for job in filtered_jobs 
                        if experience_level.lower() == job['experience_level'].lower()]
    
    # Update job data to match frontend expectations
    for job in filtered_jobs:
        job['skills_required'] = job.pop('requirements', [])
        job['source'] = 'api'
        job['is_remote'] = job['job_type'].lower() == 'remote' or 'remote' in job['location'].lower()
        job['posted_date'] = job['posted_date']
    
    # Return jobs array directly (what frontend expects)
    return Response(filtered_jobs)

@api_view(['GET'])
def jobs_detail(request, job_id):
    """Get specific job details"""
    # Sample job detail - in a real app, this would come from a database
    sample_jobs = {
        'a1b2c3d4-e5f6-7890-abcd-ef1234567890': {
            'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
            'title': 'Senior Software Engineer',
            'company': 'TechCorp Inc.',
            'location': 'San Francisco, CA',
            'job_type': 'Full-time',
            'experience_level': 'Senior',
            'salary_min': 150000,
            'salary_max': 200000,
            'description': '''We are looking for a senior software engineer to join our team and help build the next generation of our platform.

Responsibilities:
• Design and develop scalable web applications
• Lead technical discussions and code reviews
• Mentor junior developers
• Collaborate with product and design teams

Benefits:
• Competitive salary and equity
• Health, dental, and vision insurance
• 401k matching
• Flexible PTO
• Remote work options''',
            'requirements': ['Python', 'Django', 'React', '5+ years experience'],
            'posted_date': '2025-09-01',
            'application_deadline': '2025-10-01',
            'company_logo': 'https://example.com/logo1.png',
            'company_size': '100-500 employees',
            'company_industry': 'Technology',
            'remote_friendly': True
        }
    }
    
    job = sample_jobs.get(str(job_id))
    if not job:
        return Response({
            'status': 'error',
            'message': 'Job not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'status': 'success',
        'job': job
    })

@api_view(['POST'])
def jobs_apply(request, job_id):
    """Apply to a specific job"""
    cover_letter = request.data.get('cover_letter', '')
    resume_id = request.data.get('resume_id', '')
    
    # In a real app, this would save the application to the database
    return Response({
        'status': 'success',
        'message': f'Successfully applied to job {job_id}',
        'application_id': f'app_{job_id}_{hash(cover_letter)}',
        'application_data': {
            'job_id': job_id,
            'cover_letter': cover_letter,
            'resume_id': resume_id,
            'applied_date': '2025-09-08',
            'status': 'submitted'
        }
    })

@api_view(['GET'])
def jobs_applications(request):
    """Get user's job applications"""
    # Sample applications data
    applications = [
        {
            'id': 'app_1_123',
            'job_id': 1,
            'job_title': 'Senior Software Engineer',
            'company': 'TechCorp Inc.',
            'applied_date': '2025-09-08',
            'status': 'submitted',
            'cover_letter': 'I am very interested in this position...',
            'resume_id': 'resume_1'
        },
        {
            'id': 'app_2_456',
            'job_id': 2,
            'job_title': 'Data Scientist',
            'company': 'DataFlow Solutions',
            'applied_date': '2025-09-07',
            'status': 'under_review',
            'cover_letter': 'My background in machine learning...',
            'resume_id': 'resume_1'
        }
    ]
    
    return Response({
        'status': 'success',
        'applications': applications,
        'total': len(applications)
    })

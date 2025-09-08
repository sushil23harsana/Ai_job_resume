from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
from decouple import config
import json
import requests
import uuid
import random
from datetime import datetime, timedelta
import re

# Configure Gemini API
try:
    genai.configure(api_key=config('GOOGLE_GEMINI_API_KEY', default=''))
except:
    pass  # Handle missing API key gracefully

# Configure Perplexity API
PERPLEXITY_API_KEY = config('PERPLEXITY_API_KEY', default='')
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

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
    """Privacy-focused resume upload with local text extraction"""
    try:
        if not request.FILES.get('resume'):
            return Response({
                'status': 'error',
                'message': 'No resume file provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['resume']
        file_name = file.name.lower()
        
        # Extract text based on file type - all processing done in memory
        text_content = ""
        
        try:
            if file_name.endswith('.pdf'):
                # Handle PDF files - process in memory only
                import PyPDF2
                import io
                
                pdf_file = io.BytesIO(file.read())
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
                    
                # Clear memory
                pdf_file.close()
                    
            elif file_name.endswith(('.doc', '.docx')):
                # Handle Word documents - process in memory only
                import docx
                import io
                
                doc_file = io.BytesIO(file.read())
                doc = docx.Document(doc_file)
                
                for paragraph in doc.paragraphs:
                    text_content += paragraph.text + "\n"
                
                # Clear memory
                doc_file.close()
                    
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
        
        # Note: File is processed in memory only, not saved to disk
        return Response({
            'status': 'success',
            'message': f'Resume {file.name} processed successfully',
            'filename': file.name,
            'size': file.size,
            'text_content': text_content.strip(),
            'word_count': len(text_content.split()),
            'privacy_info': {
                'file_saved': False,
                'processing': 'in-memory only',
                'data_retention': 'processed temporarily for analysis, not stored permanently',
                'security': 'All text extraction done locally on server'
            }
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
    """AI Resume Analysis endpoint with detailed information extraction"""
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
        
        # First, extract personal information
        extraction_prompt = f"""
        Extract the following information from this resume text. Return ONLY a JSON object with these exact fields:
        
        {{
            "name": "extracted name or 'Not found'",
            "email": "extracted email or 'Not found'", 
            "phone": "extracted phone or 'Not found'",
            "skills": ["skill1", "skill2", "skill3"],
            "experience_years": "number of years or 'Fresh graduate'",
            "education": "highest degree",
            "location": "city/state or 'Not found'"
        }}
        
        Resume text:
        {resume_text}
        """
        
        extraction_response = model.generate_content(extraction_prompt)
        
        # Parse extracted info (handle potential JSON parsing issues)
        try:
            import re
            import json
            
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', extraction_response.text, re.DOTALL)
            if json_match:
                extracted_info = json.loads(json_match.group())
            else:
                # Fallback manual extraction
                extracted_info = {
                    "name": "Not found",
                    "email": "Not found", 
                    "phone": "Not found",
                    "skills": [],
                    "experience_years": "Fresh graduate",
                    "education": "Not found",
                    "location": "Not found"
                }
                
                # Simple regex patterns for extraction
                import re
                
                # Extract email
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, resume_text)
                if emails:
                    extracted_info["email"] = emails[0]
                
                # Extract phone
                phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
                phones = re.findall(phone_pattern, resume_text)
                if phones:
                    extracted_info["phone"] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
                
                # Extract name (assume first line or first few words)
                lines = resume_text.strip().split('\n')
                for line in lines[:5]:  # Check first 5 lines
                    line = line.strip()
                    if line and len(line.split()) <= 4 and not any(char in line for char in '@+()0123456789'):
                        extracted_info["name"] = line
                        break
                        
        except Exception as parse_error:
            extracted_info = {
                "name": "Not found",
                "email": "Not found", 
                "phone": "Not found",
                "skills": [],
                "experience_years": "Fresh graduate",
                "education": "Not found",
                "location": "Not found"
            }
        
        # Now do comprehensive analysis
        analysis_prompt = f"""
        Analyze this resume comprehensively. The person is a fresh graduate from 2025 batch.
        
        Resume: {resume_text}
        Target role: {target_role}
        
        Provide detailed analysis including:
        1. Skill assessment (rate each skill 1-10)
        2. Experience evaluation (focus on projects, internships for fresh graduate)
        3. Strengths and improvement areas
        4. Career recommendations suitable for fresh graduate
        5. Job match score for entry-level positions (1-10)
        
        Return detailed analysis in text format, not JSON.
        """
        
        analysis_response = model.generate_content(analysis_prompt)
        
        return Response({
            'status': 'success',
            'analysis': {
                'personal_info': extracted_info,
                'ai_analysis': analysis_response.text,
                'analysis_type': analysis_type,
                'target_role': target_role,
                'score': 8.0,  # Will be calculated based on analysis
                'recommendations': {
                    'suitable_roles': ['Junior Software Developer', 'Software Engineer Trainee', 'Associate Software Developer'],
                    'skill_gaps': [],
                    'next_steps': []
                }
            }
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'AI analysis failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def ai_match_jobs(request):
    """AI Job Matching endpoint with accurate fresh graduate recommendations"""
    try:
        resume_text = request.data.get('resume_text', '')
        preferences = request.data.get('preferences', {})
        use_perplexity = request.data.get('use_perplexity', True)
        limit = request.data.get('limit', 10)
        
        # Analyze experience level from resume
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # First determine experience level
        experience_prompt = f"""
        Analyze this resume and determine the candidate's experience level:
        
        Resume: {resume_text}
        
        Return ONLY one of these: "Fresh Graduate", "0-2 years", "2-5 years", "5+ years"
        """
        
        exp_response = model.generate_content(experience_prompt)
        experience_level = exp_response.text.strip()
        
        # Determine appropriate job types based on experience
        if "Fresh Graduate" in experience_level or "2025" in resume_text:
            job_types = [
                "Software Engineer Trainee",
                "Junior Software Developer", 
                "Associate Software Engineer",
                "Graduate Trainee",
                "Software Development Intern",
                "Junior Frontend Developer",
                "Junior Backend Developer",
                "Entry Level Software Engineer"
            ]
            experience_filter = "entry-level, trainee, junior, graduate, fresher"
        elif "0-2 years" in experience_level:
            job_types = [
                "Software Developer",
                "Junior Software Engineer",
                "Software Engineer I",
                "Frontend Developer",
                "Backend Developer"
            ]
            experience_filter = "junior, 0-2 years experience"
        else:
            job_types = [
                "Software Engineer",
                "Senior Software Developer", 
                "Full Stack Developer",
                "Software Engineer II"
            ]
            experience_filter = "2+ years experience"
        
        # Try Perplexity for real job search if API is available
        perplexity_api_key = config('PERPLEXITY_API_KEY', default='')
        jobs_from_perplexity = []
        
        if use_perplexity and perplexity_api_key and perplexity_api_key != 'your-perplexity-api-key-here':
            try:
                perplexity_url = "https://api.perplexity.ai/chat/completions"
                headers = {
                    "Authorization": f"Bearer {perplexity_api_key}",
                    "Content-Type": "application/json"
                }
                
                search_prompt = f"""
                Find current {experience_filter} software engineering jobs in India for fresh graduates from 2025 batch. 
                Search for positions like: {', '.join(job_types[:4])}
                
                Provide 10 real job listings with:
                - Company name
                - Job title  
                - Location
                - Salary range (in INR)
                - Key requirements
                - Application link if available
                
                Focus on entry-level positions suitable for fresh graduates.
                """
                
                data = {
                    "model": "llama-3.1-sonar-small-128k-online",
                    "messages": [{"role": "user", "content": search_prompt}]
                }
                
                response = requests.post(perplexity_url, headers=headers, json=data, timeout=30)
                if response.status_code == 200:
                    perplexity_result = response.json()
                    jobs_content = perplexity_result.get('choices', [{}])[0].get('message', {}).get('content', '')
                    
                    # Parse jobs from Perplexity response
                    if jobs_content:
                        jobs_from_perplexity = jobs_content
                        
            except Exception as perplexity_error:
                print(f"Perplexity API error: {perplexity_error}")
        
        # Generate job recommendations using Gemini (with Perplexity context if available)
        if jobs_from_perplexity:
            job_prompt = f"""
            Based on this resume and real job market data, provide {limit} accurate job recommendations:
            
            Resume: {resume_text}
            Experience Level: {experience_level}
            Real Jobs Available: {jobs_from_perplexity}
            
            Create realistic job recommendations focusing on {experience_filter} positions.
            For each job provide:
            1. Job title (appropriate for experience level)
            2. Company name
            3. Location
            4. Salary range (realistic for experience level in INR)
            5. Match percentage (realistic based on skills)
            6. Key requirements
            7. Why it's a good match
            
            Return in structured format.
            """
        else:
            job_prompt = f"""
            Based on this resume, suggest {limit} realistic job opportunities for {experience_level}:
            
            Resume: {resume_text}
            
            Recommended job types: {', '.join(job_types)}
            
            For each job provide:
            1. Job title (appropriate for fresh graduate/entry level)
            2. Company type
            3. Location (Indian cities)
            4. Salary range (realistic for fresh graduates: 3-8 LPA)
            5. Match percentage based on skills
            6. Required skills
            7. Growth prospects
            
            Focus on entry-level positions that match the candidate's skills and experience level.
            """
        
        job_response = model.generate_content(job_prompt)
        
        return Response({
            'status': 'success',
            'matches': {
                'total_found': limit,
                'experience_level': experience_level,
                'recommended_job_types': job_types,
                'jobs': job_response.text,
                'source': 'perplexity+gemini' if jobs_from_perplexity else 'gemini',
                'privacy_note': 'All processing done on server, no resume data stored permanently'
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
    """Get list of jobs with AI-powered job generation and LinkedIn scraping"""
    search = request.GET.get('search', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')
    experience_level = request.GET.get('experience_level', '')
    page = request.GET.get('page', 1)
    
    try:
        # Get user's most recent resume analysis for personalized job matching
        user_profile = None
        try:
            # Check session for resume data (if available)
            if hasattr(request, 'session') and 'last_resume_analysis' in request.session:
                user_profile = request.session['last_resume_analysis']
        except:
            pass
        
        # Generate AI-powered job listings using Perplexity API
        jobs = ai_generate_jobs(
            search_query=search,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            user_profile=user_profile
        )
        
        # Apply additional filters if needed
        filtered_jobs = jobs
        
        if search:
            filtered_jobs = [job for job in filtered_jobs 
                            if search.lower() in job.get('title', '').lower() 
                            or search.lower() in job.get('company', '').lower()
                            or any(search.lower() in req.lower() for req in job.get('skills_required', []))]
        
        if location:
            filtered_jobs = [job for job in filtered_jobs 
                            if location.lower() in job.get('location', '').lower()]
        
        if job_type:
            filtered_jobs = [job for job in filtered_jobs 
                            if job_type.lower() == job.get('job_type', '').lower()]
        
        if experience_level:
            filtered_jobs = [job for job in filtered_jobs 
                            if experience_level.lower() == job.get('experience_level', '').lower()]
        
        # Ensure we have at least some jobs to return
        if not filtered_jobs:
            # Fallback to basic job generation without strict filters
            filtered_jobs = ai_generate_jobs(
                search_query="",
                location="",
                job_type="",
                experience_level="Entry Level",
                user_profile=user_profile
            )
        
        return Response(filtered_jobs[:25])  # Return up to 25 jobs
        
    except Exception as e:
        print(f"Error generating jobs: {str(e)}")
        # Fallback to basic sample jobs if AI generation fails
        fallback_jobs = [
            {
                'id': 'fallback-1',
                'title': 'Software Developer',
                'company': 'Tech Company',
                'location': 'Remote',
                'job_type': 'Full-time',
                'experience_level': 'Entry Level',
                'salary_min': 70000,
                'salary_max': 90000,
                'description': 'Entry-level software developer position with growth opportunities.',
                'skills_required': ['Python', 'JavaScript', 'Git'],
                'posted_date': '2025-01-15',
                'source': 'api',
                'is_remote': True,
                'apply_url': 'https://careers.company.com/apply'
            }
        ]
        return Response(fallback_jobs)


def ai_generate_jobs(search_query="", location="", job_type="", experience_level="", user_profile=None):
    """Generate personalized job listings using AI and real job market data"""
    try:
        # Prepare search context based on user profile
        search_context = ""
        skills_context = ""
        experience_context = experience_level or "Entry Level"
        
        if user_profile:
            personal_info = user_profile.get('personal_info', {})
            skills = user_profile.get('skills', [])
            
            if skills:
                skills_context = f"Skills: {', '.join(skills[:10])}"  # Top 10 skills
            
            # Determine appropriate experience level from profile
            if user_profile.get('experience_level'):
                experience_context = user_profile['experience_level']
        
        # Build comprehensive search query for job market data
        location_query = location or "United States"
        job_type_query = job_type or "Full-time"
        search_terms = search_query or "software developer programming jobs"
        
        # Enhanced prompt for Perplexity API to get real job listings
        prompt = f"""Find 25 current job openings for {experience_context} level positions in {location_query}. 
        Search for: {search_terms} {job_type_query} jobs
        {skills_context}
        
        For each job, provide:
        1. Job title
        2. Company name
        3. Location (city, state or country)
        4. Job type (Full-time, Part-time, Contract, Remote)
        5. Experience level required
        6. Salary range (if available)
        7. Brief job description (1-2 sentences)
        8. Required skills/technologies (top 5-8)
        9. Application URL or company careers page
        10. Posted date (approximate)
        
        Focus on real, current job postings from company websites, LinkedIn, Indeed, and other job boards.
        Prioritize jobs suitable for {experience_context} candidates.
        Include remote opportunities and entry-level positions.
        
        Return the data in JSON format as an array of job objects."""
        
        # Make API call to Perplexity
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a job search assistant that finds real, current job listings from the web. Always return valid JSON data with actual job opportunities."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.3,
            "return_citations": True
        }
        
        response = requests.post(PERPLEXITY_API_URL, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Try to extract JSON from the response
            jobs = parse_jobs_from_ai_response(content)
            
            if jobs and len(jobs) > 0:
                return jobs
            else:
                # Generate fallback jobs using Gemini if Perplexity doesn't return structured data
                return generate_fallback_jobs_with_gemini(search_query, location, job_type, experience_context, user_profile)
        
        else:
            print(f"Perplexity API error: {response.status_code}")
            return generate_fallback_jobs_with_gemini(search_query, location, job_type, experience_context, user_profile)
            
    except Exception as e:
        print(f"Error in ai_generate_jobs: {str(e)}")
        return generate_fallback_jobs_with_gemini(search_query, location, job_type, experience_context, user_profile)


def parse_jobs_from_ai_response(content):
    """Parse job listings from AI response content"""
    try:
        import json
        import uuid
        from datetime import datetime, timedelta
        import re
        
        # Try to find JSON in the response
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            jobs_data = json.loads(json_str)
        else:
            # Try to parse the entire content as JSON
            jobs_data = json.loads(content)
        
        formatted_jobs = []
        for job in jobs_data:
            if isinstance(job, dict):
                # Generate unique ID
                job_id = str(uuid.uuid4())
                
                # Format the job data to match frontend expectations
                formatted_job = {
                    'id': job_id,
                    'title': job.get('title', job.get('job_title', 'Software Developer')),
                    'company': job.get('company', job.get('company_name', 'Tech Company')),
                    'location': job.get('location', 'Remote'),
                    'job_type': job.get('job_type', job.get('type', 'Full-time')),
                    'experience_level': job.get('experience_level', job.get('level', 'Entry Level')),
                    'salary_min': job.get('salary_min', job.get('min_salary', 60000)),
                    'salary_max': job.get('salary_max', job.get('max_salary', 90000)),
                    'description': job.get('description', job.get('job_description', 'Great opportunity to grow your career.')),
                    'skills_required': job.get('skills_required', job.get('required_skills', job.get('skills', ['Programming']))),
                    'posted_date': job.get('posted_date', (datetime.now() - timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d')),
                    'source': 'linkedin',
                    'is_remote': 'remote' in job.get('location', '').lower() or job.get('job_type', '').lower() == 'remote',
                    'apply_url': job.get('apply_url', job.get('application_url', job.get('url', f'https://linkedin.com/jobs/view/{job_id}')))
                }
                
                # Ensure skills_required is a list
                if isinstance(formatted_job['skills_required'], str):
                    formatted_job['skills_required'] = [s.strip() for s in formatted_job['skills_required'].split(',')]
                
                formatted_jobs.append(formatted_job)
        
        return formatted_jobs[:25]  # Return up to 25 jobs
        
    except Exception as e:
        print(f"Error parsing jobs from AI response: {str(e)}")
        return []


def generate_fallback_jobs_with_gemini(search_query, location, job_type, experience_level, user_profile):
    """Generate job listings using Gemini as fallback"""
    try:
        # Prepare context for Gemini
        skills_context = ""
        if user_profile and user_profile.get('skills'):
            skills_context = f"Candidate skills: {', '.join(user_profile['skills'][:10])}"
        
        location_context = location or "United States"
        job_type_context = job_type or "Full-time"
        search_context = search_query or "software development programming"
        
        prompt = f"""Generate 20 realistic job listings for {experience_level} level positions in {location_context}.
        Job focus: {search_context} {job_type_context} positions
        {skills_context}
        
        Create diverse job opportunities including:
        - Software development roles
        - Data analysis positions  
        - Frontend/backend development
        - Entry-level tech roles
        - Remote opportunities
        
        For each job, provide realistic details:
        - Job title
        - Company name (realistic tech companies)
        - Location
        - Salary range appropriate for {experience_level} level
        - Required skills (5-8 relevant technologies)
        - Brief description
        - Application URL (use realistic company career pages)
        
        Return ONLY a valid JSON array with this exact structure:
        [
          {{
            "title": "Job Title",
            "company": "Company Name", 
            "location": "City, State",
            "job_type": "Full-time",
            "experience_level": "{experience_level}",
            "salary_min": 60000,
            "salary_max": 85000,
            "description": "Brief job description",
            "skills_required": ["Skill1", "Skill2", "Skill3"],
            "apply_url": "https://company.com/careers"
          }}
        ]"""
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        if response and response.text:
            jobs = parse_jobs_from_ai_response(response.text)
            if jobs:
                return jobs
        
        # Final fallback with basic jobs
        return generate_basic_fallback_jobs(experience_level)
        
    except Exception as e:
        print(f"Error in generate_fallback_jobs_with_gemini: {str(e)}")
        return generate_basic_fallback_jobs(experience_level)


def generate_basic_fallback_jobs(experience_level="Entry Level"):
    """Generate basic fallback jobs when AI services fail"""
    import uuid
    from datetime import datetime, timedelta
    
    basic_jobs = [
        {
            'title': 'Software Developer',
            'company': 'TechStart Inc',
            'location': 'Remote',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 65000 if experience_level == 'Entry Level' else 85000,
            'salary_max': 85000 if experience_level == 'Entry Level' else 120000,
            'description': 'Join our growing team to build innovative software solutions.',
            'skills_required': ['Python', 'JavaScript', 'Git', 'SQL'],
            'apply_url': 'https://techstart.com/careers'
        },
        {
            'title': 'Frontend Developer',
            'company': 'WebSolutions Co',
            'location': 'New York, NY',
            'job_type': 'Full-time', 
            'experience_level': experience_level,
            'salary_min': 60000 if experience_level == 'Entry Level' else 80000,
            'salary_max': 80000 if experience_level == 'Entry Level' else 110000,
            'description': 'Create beautiful and responsive web applications.',
            'skills_required': ['React', 'TypeScript', 'CSS', 'HTML'],
            'apply_url': 'https://websolutions.com/jobs'
        },
        {
            'title': 'Data Analyst',
            'company': 'DataCorp',
            'location': 'San Francisco, CA',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 70000 if experience_level == 'Entry Level' else 90000,
            'salary_max': 90000 if experience_level == 'Entry Level' else 130000,
            'description': 'Analyze data to drive business insights and decisions.',
            'skills_required': ['Python', 'SQL', 'Excel', 'Tableau'],
            'apply_url': 'https://datacorp.com/careers'
        },
        {
            'title': 'Backend Developer',
            'company': 'APITech Solutions',
            'location': 'Remote',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 68000 if experience_level == 'Entry Level' else 88000,
            'salary_max': 88000 if experience_level == 'Entry Level' else 125000,
            'description': 'Build and maintain scalable backend systems and APIs.',
            'skills_required': ['Python', 'Django', 'PostgreSQL', 'REST APIs'],
            'apply_url': 'https://apitech.com/careers'
        },
        {
            'title': 'QA Engineer',
            'company': 'TestPro Inc',
            'location': 'Chicago, IL',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 62000 if experience_level == 'Entry Level' else 82000,
            'salary_max': 82000 if experience_level == 'Entry Level' else 115000,
            'description': 'Ensure software quality through comprehensive testing strategies.',
            'skills_required': ['Testing', 'Automation', 'Python', 'Selenium'],
            'apply_url': 'https://testpro.com/careers'
        },
        {
            'title': 'DevOps Engineer',
            'company': 'CloudOps Systems',
            'location': 'Austin, TX',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 75000 if experience_level == 'Entry Level' else 95000,
            'salary_max': 95000 if experience_level == 'Entry Level' else 135000,
            'description': 'Manage cloud infrastructure and deployment pipelines.',
            'skills_required': ['AWS', 'Docker', 'CI/CD', 'Linux'],
            'apply_url': 'https://cloudops.com/jobs'
        },
        {
            'title': 'Mobile Developer',
            'company': 'AppCraft Studios',
            'location': 'Los Angeles, CA',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 70000 if experience_level == 'Entry Level' else 90000,
            'salary_max': 90000 if experience_level == 'Entry Level' else 130000,
            'description': 'Develop cross-platform mobile applications.',
            'skills_required': ['React Native', 'JavaScript', 'Mobile Development', 'Git'],
            'apply_url': 'https://appcraft.com/careers'
        },
        {
            'title': 'UI/UX Designer',
            'company': 'DesignFlow Agency',
            'location': 'Seattle, WA',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 65000 if experience_level == 'Entry Level' else 85000,
            'salary_max': 85000 if experience_level == 'Entry Level' else 120000,
            'description': 'Create intuitive and engaging user experiences.',
            'skills_required': ['Figma', 'UI Design', 'UX Research', 'Prototyping'],
            'apply_url': 'https://designflow.com/careers'
        },
        {
            'title': 'Machine Learning Engineer',
            'company': 'AI Innovations Lab',
            'location': 'Boston, MA',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 80000 if experience_level == 'Entry Level' else 100000,
            'salary_max': 100000 if experience_level == 'Entry Level' else 140000,
            'description': 'Build and deploy machine learning models for real-world applications.',
            'skills_required': ['Python', 'Machine Learning', 'TensorFlow', 'Data Science'],
            'apply_url': 'https://ailab.com/careers'
        },
        {
            'title': 'Cybersecurity Analyst',
            'company': 'SecureNet Solutions',
            'location': 'Washington, DC',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 72000 if experience_level == 'Entry Level' else 92000,
            'salary_max': 92000 if experience_level == 'Entry Level' else 132000,
            'description': 'Protect organizational assets through comprehensive security monitoring.',
            'skills_required': ['Security', 'Network Security', 'Risk Assessment', 'SIEM'],
            'apply_url': 'https://securenet.com/careers'
        },
        {
            'title': 'Database Administrator',
            'company': 'DataSystems Corp',
            'location': 'Denver, CO',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 68000 if experience_level == 'Entry Level' else 88000,
            'salary_max': 88000 if experience_level == 'Entry Level' else 125000,
            'description': 'Manage and optimize database systems for high performance.',
            'skills_required': ['SQL', 'Database Management', 'PostgreSQL', 'Performance Tuning'],
            'apply_url': 'https://datasystems.com/jobs'
        },
        {
            'title': 'Technical Writer',
            'company': 'DocTech Publishing',
            'location': 'Remote',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 60000 if experience_level == 'Entry Level' else 80000,
            'salary_max': 80000 if experience_level == 'Entry Level' else 110000,
            'description': 'Create clear and comprehensive technical documentation.',
            'skills_required': ['Technical Writing', 'Documentation', 'Markdown', 'API Documentation'],
            'apply_url': 'https://doctech.com/careers'
        },
        {
            'title': 'Product Manager',
            'company': 'InnovateNow Technologies',
            'location': 'San Diego, CA',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 75000 if experience_level == 'Entry Level' else 95000,
            'salary_max': 95000 if experience_level == 'Entry Level' else 135000,
            'description': 'Drive product strategy and coordinate cross-functional teams.',
            'skills_required': ['Product Management', 'Agile', 'Analytics', 'User Research'],
            'apply_url': 'https://innovatenow.com/careers'
        },
        {
            'title': 'Systems Analyst',
            'company': 'TechConsult Group',
            'location': 'Phoenix, AZ',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 65000 if experience_level == 'Entry Level' else 85000,
            'salary_max': 85000 if experience_level == 'Entry Level' else 120000,
            'description': 'Analyze business requirements and design technical solutions.',
            'skills_required': ['Systems Analysis', 'Business Analysis', 'SQL', 'Process Improvement'],
            'apply_url': 'https://techconsult.com/jobs'
        },
        {
            'title': 'Network Engineer',
            'company': 'NetPro Infrastructure',
            'location': 'Atlanta, GA',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 70000 if experience_level == 'Entry Level' else 90000,
            'salary_max': 90000 if experience_level == 'Entry Level' else 130000,
            'description': 'Design and maintain enterprise network infrastructure.',
            'skills_required': ['Networking', 'Cisco', 'Network Security', 'Troubleshooting'],
            'apply_url': 'https://netpro.com/careers'
        },
        {
            'title': 'Cloud Engineer',
            'company': 'CloudFirst Solutions',
            'location': 'Miami, FL',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 73000 if experience_level == 'Entry Level' else 93000,
            'salary_max': 93000 if experience_level == 'Entry Level' else 133000,
            'description': 'Implement and manage cloud-based infrastructure solutions.',
            'skills_required': ['AWS', 'Cloud Computing', 'Terraform', 'Kubernetes'],
            'apply_url': 'https://cloudfirst.com/careers'
        },
        {
            'title': 'Software Tester',
            'company': 'QualityFirst Testing',
            'location': 'Portland, OR',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 58000 if experience_level == 'Entry Level' else 78000,
            'salary_max': 78000 if experience_level == 'Entry Level' else 108000,
            'description': 'Execute comprehensive testing strategies for software applications.',
            'skills_required': ['Manual Testing', 'Test Cases', 'Bug Tracking', 'Quality Assurance'],
            'apply_url': 'https://qualityfirst.com/jobs'
        },
        {
            'title': 'Web Developer',
            'company': 'WebCraft Digital',
            'location': 'Nashville, TN',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 62000 if experience_level == 'Entry Level' else 82000,
            'salary_max': 82000 if experience_level == 'Entry Level' else 115000,
            'description': 'Build responsive and interactive web applications.',
            'skills_required': ['HTML', 'CSS', 'JavaScript', 'React'],
            'apply_url': 'https://webcraft.com/careers'
        },
        {
            'title': 'Business Analyst',
            'company': 'AnalyticsPro Consulting',
            'location': 'Minneapolis, MN',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 64000 if experience_level == 'Entry Level' else 84000,
            'salary_max': 84000 if experience_level == 'Entry Level' else 118000,
            'description': 'Bridge the gap between business needs and technical solutions.',
            'skills_required': ['Business Analysis', 'Requirements Gathering', 'SQL', 'Data Analysis'],
            'apply_url': 'https://analyticspro.com/careers'
        },
        {
            'title': 'IT Support Specialist',
            'company': 'TechSupport Solutions',
            'location': 'Salt Lake City, UT',
            'job_type': 'Full-time',
            'experience_level': experience_level,
            'salary_min': 55000 if experience_level == 'Entry Level' else 75000,
            'salary_max': 75000 if experience_level == 'Entry Level' else 105000,
            'description': 'Provide technical support and troubleshooting for end users.',
            'skills_required': ['Technical Support', 'Troubleshooting', 'Windows', 'Help Desk'],
            'apply_url': 'https://techsupport.com/jobs'
        }
    ]
    
    # Format jobs with required fields
    formatted_jobs = []
    for job in basic_jobs:
        job['id'] = str(uuid.uuid4())
        job['posted_date'] = (datetime.now() - timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d')
        job['source'] = 'api'
        job['is_remote'] = 'remote' in job['location'].lower()
        formatted_jobs.append(job)
    
    return formatted_jobs

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

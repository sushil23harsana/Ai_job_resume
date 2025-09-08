# AI Resume-to-Jobs Platform 🚀

A comprehensive AI-powered platform that analyzes resumes using advanced AI technology and automatically finds matching job opportunities using **LEGAL** data sources and smart collection methods.

## ⚖️ Legal & Smart Data Collection

**This platform uses innovative legal data collection methods:**
- ✅ **Smart LinkedIn Strategy**: Use Perplexity AI to find LinkedIn URLs, then extract specific job data
- ✅ **Custom Perplexity Client**: Direct API integration using requests library (no dependency issues)
- ✅ Official job board APIs (Adzuna, USAJobs, Reed)
- ✅ Public RSS feeds and government job databases
- ✅ Partner program integrations
- ❌ NO mass web scraping or Terms of Service violations

## 🧠 AI Services

### Core AI Stack
- **Google Gemini Pro**: Resume analysis, job matching, career advice
- **Perplexity AI**: Real-time market research, company insights, smart job discovery
- **Custom Integration**: Requests-based Perplexity client for reliability

### Smart LinkedIn Collection
Our innovative approach:
1. **Perplexity Discovery**: Use AI to search for jobs and get LinkedIn URLs
2. **Targeted Extraction**: Extract data only from specific job pages  
3. **Legal Compliance**: No mass scraping, respects rate limits
4. **High Quality**: Gets the most relevant and recent job postings

## 🌟 Features

### Core Functionality
- **AI Resume Parsing**: Advanced extraction using Google Gemini Pro
- **Smart Job Matching**: AI-powered compatibility scoring
- **Legal Job Aggregation**: Data from 20+ countries via official APIs
- **Perplexity AI Integration**: Real-time market intelligence
- **Career Analytics**: Market trends and salary insights

### AI-Powered Capabilities
- Resume optimization recommendations
- Skill gap analysis and learning paths
- Real-time market trend analysis
- Interview preparation assistance
- Personalized career roadmaps

### Platform Features
- Modern React frontend with responsive design
- Robust Django REST API backend
- PostgreSQL database with optimized queries
- Redis caching for performance
- Celery background task processing
- JWT authentication with refresh tokens
- Real-time job alerts and notifications

## 🏗️ Legal-First Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React.js      │    │   Django REST    │    │  PostgreSQL     │
│   Frontend      │◄──►│   API Backend    │◄──►│   Database      │
│   (Port 3000)   │    │   (Port 8000)    │    │   (Port 5432)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│     Redis       │    │     Celery       │    │   LEGAL APIs    │
│    Cache        │◄──►│  Task Queue      │◄──►│ Adzuna, USAJobs │
│   (Port 6379)   │    │  (Background)    │    │ RSS, Perplexity │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 🔒 Legal Data Sources
- **Adzuna API**: 20+ countries, 1M+ jobs, completely legal
- **USAJobs**: US government positions (public domain)
- **RSS Feeds**: Stack Overflow, AngelList, RemoteOK
- **Partner APIs**: Indeed Publisher Program, ZipRecruiter
- **Government DBs**: Public job databases worldwide

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+

### Backend Setup

1. **Clone and Navigate**
   ```bash
   git clone <your-repository>
   cd JobApply
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\\Scripts\\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb resume_ai_platform
   
   # Run migrations
   cd resume_ai_backend
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Initialize Platform**
   ```bash
   python manage.py init_platform --create-superuser --load-skills --load-sample-data
   ```

7. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to Frontend**
   ```bash
   cd ../frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm start
   ```

### Background Services

1. **Start Redis**
   ```bash
   redis-server
   ```

2. **Start Celery Worker**
   ```bash
   cd resume_ai_backend
   celery -A resume_ai_backend worker --loglevel=info
   ```

3. **Start Celery Beat (Scheduler)**
   ```bash
   celery -A resume_ai_backend beat --loglevel=info
   ```

## 📁 Project Structure

```
JobApply/
├── resume_ai_backend/          # Django Backend
│   ├── resume_ai_backend/      # Main Django project
│   ├── authentication/        # User management
│   ├── resumes/              # Resume processing
│   ├── jobs/                 # Job aggregation
│   ├── ai_services/          # AI processing services
│   ├── media/                # User uploads
│   ├── static/               # Static files
│   └── manage.py
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── utils/           # Utilities
│   │   └── styles/          # CSS/Styling
│   ├── public/
│   └── package.json
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```env
# Django Configuration
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_NAME=resume_ai_platform
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://127.0.0.1:6379/1

# AI Services
OPENAI_API_KEY=your-openai-key
PERPLEXITY_API_KEY=your-perplexity-key

# Job Platform Credentials (Optional)
LINKEDIN_EMAIL=your-email
LINKEDIN_PASSWORD=your-password
NAUKRI_EMAIL=your-email
NAUKRI_PASSWORD=your-password

# Email Configuration
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-app-password
```

## 🧠 AI Services Integration

### Perplexity AI Setup
1. Get API key from [Perplexity AI](https://www.perplexity.ai)
2. Add to environment variables
3. Configure domain filters for job searches

### OpenAI Integration
1. Get API key from [OpenAI](https://platform.openai.com)
2. Configure for resume analysis and optimization
3. Set up usage limits and monitoring

## 📊 API Documentation

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Token refresh
- `POST /api/auth/logout/` - User logout

### Resume Processing
- `POST /api/resumes/upload/` - Upload resume
- `GET /api/resumes/{id}/parsed-data/` - Get parsed data
- `POST /api/resumes/{id}/analyze/` - AI analysis
- `GET /api/resumes/{id}/suggestions/` - Improvement suggestions

### Job Management
- `GET /api/jobs/search/` - Search jobs
- `POST /api/jobs/match/` - Find matching jobs
- `POST /api/jobs/{id}/save/` - Save job
- `POST /api/jobs/{id}/apply/` - Apply to job

### AI Services
- `POST /api/ai/parse-resume/` - Parse resume with AI
- `POST /api/ai/match-jobs/` - AI job matching
- `POST /api/ai/perplexity/search-jobs/` - Perplexity job search
- `POST /api/ai/career-advice/` - Generate career advice

## 🔒 Security Features

- JWT token authentication
- Password encryption with bcrypt
- CORS protection
- Rate limiting
- Input validation and sanitization
- File upload security
- SQL injection protection

## 📈 Performance Optimization

- Database query optimization
- Redis caching
- Background task processing
- Image optimization
- API response compression
- CDN for static files

## 🧪 Testing

```bash
# Run backend tests
cd resume_ai_backend
python manage.py test

# Run frontend tests
cd frontend
npm test

# Run integration tests
npm run test:integration
```

## 🚀 Deployment

### Production Setup

1. **Environment Configuration**
   ```bash
   # Set production environment variables
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com
   ```

2. **Database Migration**
   ```bash
   python manage.py migrate --settings=resume_ai_backend.settings.production
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Deploy with Gunicorn**
   ```bash
   gunicorn resume_ai_backend.wsgi:application --bind 0.0.0.0:8000
   ```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Email: support@yourplatform.com
- Documentation: [Link to detailed docs]

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Core resume parsing
- ✅ Basic job matching
- ✅ LinkedIn/Naukri integration
- ✅ Perplexity AI integration

### Phase 2 (Upcoming)
- 🔄 Advanced AI recommendations
- 🔄 Real-time job alerts
- 🔄 Interview preparation tools
- 🔄 Mobile app development

### Phase 3 (Future)
- 📋 Recruiter dashboard
- 📋 Company analytics
- 📋 Advanced market insights
- 📋 Integration with more job platforms

---

**Built with ❤️ using Django, React, and AI technologies**

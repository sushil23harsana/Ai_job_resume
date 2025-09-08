import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRightIcon, DocumentTextIcon, BriefcaseIcon, ChartBarIcon, SparklesIcon } from '@heroicons/react/24/outline';

const HomePage: React.FC = () => {
  const features = [
    {
      icon: DocumentTextIcon,
      title: 'AI Resume Analysis',
      description: 'Upload your resume and get detailed AI-powered analysis using Google Gemini Pro for skills, experience, and career potential.'
    },
    {
      icon: BriefcaseIcon,
      title: 'Smart Job Matching',
      description: 'Find perfect job opportunities using our smart LinkedIn collection via Perplexity AI and legal job sources.'
    },
    {
      icon: ChartBarIcon,
      title: 'Market Insights',
      description: 'Get real-time market research, salary insights, and company analysis powered by Perplexity AI.'
    },
    {
      icon: SparklesIcon,
      title: 'Career Guidance',
      description: 'Receive personalized career advice and growth recommendations based on your profile and market trends.'
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              AI-Powered Resume to Jobs Platform
            </h1>
            <p className="text-xl text-indigo-100 mb-8 max-w-3xl mx-auto">
              Upload your resume, get AI analysis with Google Gemini Pro, and discover perfect job matches 
              from LinkedIn and top job boards using smart, legal collection methods.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/upload"
                className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50 transition-colors"
              >
                Upload Resume
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </Link>
              <Link
                to="/jobs"
                className="inline-flex items-center px-8 py-3 border border-white text-base font-medium rounded-md text-white hover:bg-white hover:text-indigo-600 transition-colors"
              >
                Browse Jobs
                <BriefcaseIcon className="ml-2 h-5 w-5" />
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How JobAI Works
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our AI-powered platform combines Google Gemini Pro and Perplexity AI to analyze your resume 
              and find the best job opportunities using smart, legal data collection.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="text-center">
                  <div className="bg-indigo-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-8 h-8 text-indigo-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* AI Technology Section */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Powered by Advanced AI
            </h2>
            <p className="text-lg text-gray-600">
              We use cutting-edge AI technologies to provide the best job matching experience.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white p-8 rounded-lg shadow-md">
              <h3 className="text-2xl font-semibold text-gray-900 mb-4">Google Gemini Pro</h3>
              <p className="text-gray-600 mb-4">
                Advanced resume analysis, skills extraction, and job matching using Google's latest AI model.
              </p>
              <ul className="text-gray-600 space-y-2">
                <li>• Intelligent resume parsing</li>
                <li>• Skills gap analysis</li>
                <li>• Career advice generation</li>
                <li>• Job compatibility scoring</li>
              </ul>
            </div>
            
            <div className="bg-white p-8 rounded-lg shadow-md">
              <h3 className="text-2xl font-semibold text-gray-900 mb-4">Perplexity AI</h3>
              <p className="text-gray-600 mb-4">
                Real-time job market research and smart LinkedIn job discovery with legal compliance.
              </p>
              <ul className="text-gray-600 space-y-2">
                <li>• Real-time market insights</li>
                <li>• Smart LinkedIn URL discovery</li>
                <li>• Company research & analysis</li>
                <li>• Salary benchmarking</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-indigo-600 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Find Your Dream Job?
          </h2>
          <p className="text-lg text-indigo-100 mb-8">
            Upload your resume now and let AI find the perfect opportunities for you.
          </p>
          <Link
            to="/upload"
            className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50 transition-colors"
          >
            Get Started Now
            <DocumentTextIcon className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

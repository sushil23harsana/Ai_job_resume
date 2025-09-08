import React, { useState, useEffect } from 'react';
import { ChartBarIcon, DocumentTextIcon, BriefcaseIcon, UserIcon, TrophyIcon } from '@heroicons/react/24/outline';
import axios from 'axios';

interface DashboardStats {
  total_resumes: number;
  total_applications: number;
  matched_jobs: number;
  ai_analysis_score: number;
}

interface RecentActivity {
  id: string;
  type: 'resume_upload' | 'job_application' | 'ai_analysis';
  description: string;
  timestamp: string;
}

const DashboardPage: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    total_resumes: 0,
    total_applications: 0,
    matched_jobs: 0,
    ai_analysis_score: 0
  });
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Mock data for now - replace with actual API calls
      setStats({
        total_resumes: 3,
        total_applications: 12,
        matched_jobs: 45,
        ai_analysis_score: 85
      });

      setRecentActivity([
        {
          id: '1',
          type: 'resume_upload',
          description: 'Uploaded new resume: Senior_Developer_Resume.pdf',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '2',
          type: 'ai_analysis',
          description: 'AI analysis completed with score: 85/100',
          timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString()
        },
        {
          id: '3',
          type: 'job_application',
          description: 'Applied to Senior Python Developer at TechCorp',
          timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
        }
      ]);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffHours = Math.ceil(diffTime / (1000 * 60 * 60));
    
    if (diffHours < 1) return 'Just now';
    if (diffHours < 24) return `${diffHours} hours ago`;
    const diffDays = Math.ceil(diffHours / 24);
    if (diffDays === 1) return '1 day ago';
    return `${diffDays} days ago`;
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'resume_upload':
        return <DocumentTextIcon className="h-5 w-5 text-blue-500" />;
      case 'job_application':
        return <BriefcaseIcon className="h-5 w-5 text-green-500" />;
      case 'ai_analysis':
        return <ChartBarIcon className="h-5 w-5 text-purple-500" />;
      default:
        return <UserIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Track your job search progress and AI-powered insights
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-blue-100">
              <DocumentTextIcon className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-500">Total Resumes</h3>
              <p className="text-2xl font-bold text-gray-900">{stats.total_resumes}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-green-100">
              <BriefcaseIcon className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-500">Applications</h3>
              <p className="text-2xl font-bold text-gray-900">{stats.total_applications}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-purple-100">
              <ChartBarIcon className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-500">Matched Jobs</h3>
              <p className="text-2xl font-bold text-gray-900">{stats.matched_jobs}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-yellow-100">
              <TrophyIcon className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-500">AI Score</h3>
              <p className="text-2xl font-bold text-gray-900">{stats.ai_analysis_score}/100</p>
            </div>
          </div>
        </div>
      </div>

      {/* Content Grid */}
      <div className="grid lg:grid-cols-3 gap-8">
        {/* Recent Activity */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Recent Activity</h2>
            
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50">
                  <div className="flex-shrink-0 mt-1">
                    {getActivityIcon(activity.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900">{activity.description}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {formatTimestamp(activity.timestamp)}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {recentActivity.length === 0 && (
              <div className="text-center py-8">
                <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <p className="text-gray-500">No recent activity</p>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
            
            <div className="space-y-3">
              <button 
                onClick={() => window.location.href = '/upload'}
                className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 transition-colors"
              >
                <div className="flex items-center">
                  <DocumentTextIcon className="h-5 w-5 text-indigo-600 mr-3" />
                  <span className="text-sm font-medium text-gray-900">Upload New Resume</span>
                </div>
              </button>
              
              <button 
                onClick={() => window.location.href = '/jobs'}
                className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 transition-colors"
              >
                <div className="flex items-center">
                  <BriefcaseIcon className="h-5 w-5 text-indigo-600 mr-3" />
                  <span className="text-sm font-medium text-gray-900">Browse Jobs</span>
                </div>
              </button>

              <button className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 transition-colors">
                <div className="flex items-center">
                  <ChartBarIcon className="h-5 w-5 text-indigo-600 mr-3" />
                  <span className="text-sm font-medium text-gray-900">Get AI Career Advice</span>
                </div>
              </button>
            </div>
          </div>

          {/* AI Score Card */}
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg shadow-md p-6 text-white">
            <h3 className="text-lg font-semibold mb-2">AI Resume Score</h3>
            <div className="flex items-center mb-4">
              <div className="text-3xl font-bold">{stats.ai_analysis_score}</div>
              <div className="text-lg ml-1">/100</div>
            </div>
            
            <div className="w-full bg-white bg-opacity-30 rounded-full h-2 mb-4">
              <div 
                className="bg-white h-2 rounded-full transition-all duration-500" 
                style={{ width: `${stats.ai_analysis_score}%` }}
              ></div>
            </div>
            
            <p className="text-sm opacity-90">
              Your resume has been analyzed by our AI. 
              {stats.ai_analysis_score >= 80 && " Excellent work!"}
              {stats.ai_analysis_score >= 60 && stats.ai_analysis_score < 80 && " Good progress!"}
              {stats.ai_analysis_score < 60 && " Room for improvement."}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;

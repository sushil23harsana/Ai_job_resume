import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { DocumentTextIcon, CloudArrowUpIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import { toast } from 'react-hot-toast';
import axios from 'axios';

interface AnalysisResult {
  personal_info?: {
    name?: string;
    email?: string;
    phone?: string;
  };
  skills?: string[];
  experience?: string[];
  education?: string[];
  ai_analysis?: {
    strengths?: string[];
    suggestions?: string[];
    score?: number;
  };
}

const UploadPage: React.FC = () => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploadedFile(file);
    setIsUploading(true);

    const formData = new FormData();
    formData.append('resume', file);

    try {
      // Upload resume
      const uploadResponse = await axios.post(
        'http://localhost:8000/api/resumes/upload/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      toast.success('Resume uploaded successfully!');
      setIsUploading(false);
      setIsAnalyzing(true);

      // Analyze resume with AI
      const analysisResponse = await axios.post(
        'http://localhost:8000/api/ai/analyze-resume/',
        {
          resume_text: uploadResponse.data.text_content,
          analysis_type: 'comprehensive'
        }
      );

      setAnalysisResult(analysisResponse.data.analysis);
      toast.success('AI analysis completed!');
    } catch (error) {
      toast.error('Failed to upload or analyze resume. Please try again.');
      console.error('Upload/Analysis error:', error);
    } finally {
      setIsUploading(false);
      setIsAnalyzing(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxSize: 5242880, // 5MB
    multiple: false
  });

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Upload Your Resume
        </h1>
        <p className="text-lg text-gray-600">
          Upload your resume and let our AI analyze it with Google Gemini Pro to find the best job matches.
        </p>
      </div>

      {/* Upload Area */}
      <div className="mb-8">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-200 ${
            isDragActive
              ? 'border-indigo-400 bg-indigo-50 scale-105'
              : uploadedFile
              ? 'border-green-400 bg-green-50'
              : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
          }`}
        >
          <input {...getInputProps()} />
          {uploadedFile ? (
            <CheckCircleIcon className="w-12 h-12 text-green-500 mx-auto mb-4" />
          ) : (
            <CloudArrowUpIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          )}
          
          {isDragActive ? (
            <p className="text-lg text-indigo-600">Drop your resume here...</p>
          ) : uploadedFile ? (
            <div>
              <p className="text-lg text-green-600 mb-2 font-medium">
                Resume uploaded successfully!
              </p>
              <p className="text-sm text-gray-500">
                Click to upload a different file
              </p>
            </div>
          ) : (
            <div>
              <p className="text-lg text-gray-600 mb-2">
                Drag and drop your resume here, or click to browse
              </p>
              <p className="text-sm text-gray-500">
                Supports PDF, DOC, DOCX files up to 5MB
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Upload Status */}
      {uploadedFile && (
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="flex items-center">
            <DocumentTextIcon className="w-8 h-8 text-indigo-600 mr-3" />
            <div className="flex-1">
              <h3 className="text-lg font-medium text-gray-900">
                {uploadedFile.name}
              </h3>
              <p className="text-sm text-gray-500">
                {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
            {(isUploading || isAnalyzing) && (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-600"></div>
                <span className="ml-2 text-sm text-gray-600">
                  {isUploading ? 'Uploading...' : 'Analyzing with AI...'}
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Analysis Results */}
      {analysisResult && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            AI Resume Analysis Complete
          </h2>
          
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Personal Information
              </h3>
              <div className="space-y-2">
                <p><span className="font-medium">Name:</span> {analysisResult.personal_info?.name || 'Not found'}</p>
                <p><span className="font-medium">Email:</span> {analysisResult.personal_info?.email || 'Not found'}</p>
                <p><span className="font-medium">Phone:</span> {analysisResult.personal_info?.phone || 'Not found'}</p>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Skills Extracted
              </h3>
              <div className="flex flex-wrap gap-2">
                {analysisResult.skills?.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {analysisResult.ai_analysis && (
            <div className="border-t pt-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                AI Analysis & Recommendations
              </h3>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Strengths</h4>
                  <ul className="text-gray-600 space-y-1">
                    {analysisResult.ai_analysis.strengths?.map((strength, index) => (
                      <li key={index}>• {strength}</li>
                    ))}
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Suggestions</h4>
                  <ul className="text-gray-600 space-y-1">
                    {analysisResult.ai_analysis.suggestions?.map((suggestion, index) => (
                      <li key={index}>• {suggestion}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {analysisResult.ai_analysis.score && (
                <div className="mt-4">
                  <div className="flex items-center">
                    <span className="text-sm font-medium text-gray-700 mr-2">Resume Score:</span>
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-indigo-600 h-2 rounded-full" 
                        style={{ width: `${analysisResult.ai_analysis.score}%` }}
                      ></div>
                    </div>
                    <span className="ml-2 text-sm font-medium text-gray-900">
                      {analysisResult.ai_analysis.score}/100
                    </span>
                  </div>
                </div>
              )}
            </div>
          )}

          <div className="mt-8 text-center">
            <button
              onClick={() => window.location.href = '/jobs'}
              className="px-8 py-3 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors font-medium"
            >
              Find Matching Jobs
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadPage;

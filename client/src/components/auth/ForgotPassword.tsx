import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { EnvelopeIcon, SparklesIcon, ArrowLeftIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

interface ForgotPasswordFormData {
  email: string;
}

interface ForgotPasswordProps {
  onBackToSignIn: () => void;
}

export const ForgotPassword: React.FC<ForgotPasswordProps> = ({ onBackToSignIn }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isEmailSent, setIsEmailSent] = useState(false);
  const [resetUrl, setResetUrl] = useState('');
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<ForgotPasswordFormData>();

  const onSubmit = async (data: ForgotPasswordFormData) => {
    try {
      setIsLoading(true);
      
      const response = await fetch('http://localhost:5000/api/auth/forgot-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const result = await response.json();
        setIsEmailSent(true);
        if (result.reset_url) {
          setResetUrl(result.reset_url);
        }
      } else {
        const errorData = await response.json();
        setError('root', {
          type: 'manual',
          message: errorData.error || 'Failed to send reset email',
        });
      }
    } catch (error: any) {
      setError('root', {
        type: 'manual',
        message: 'Network error. Please try again.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isEmailSent) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-800 flex items-center justify-center p-4">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
          <div className="absolute top-40 left-40 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
        </div>

        <div className="relative z-10 w-full max-w-md">
          {/* Glass Morphism Container */}
          <div className="backdrop-blur-lg bg-white/10 rounded-3xl p-8 shadow-2xl border border-white/20">
            {/* Header */}
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-green-500 to-blue-500 rounded-2xl mb-4 shadow-lg">
                <CheckCircleIcon className="w-8 h-8 text-white" />
              </div>
              <h1 className="text-3xl font-bold text-white mb-2">Check Your Email</h1>
              <p className="text-blue-200">We've sent password reset instructions to your email address.</p>
            </div>

            {/* Development Reset Link */}
            {resetUrl && (
              <div className="mb-6 p-4 bg-yellow-500/20 border border-yellow-500/30 rounded-xl backdrop-blur-sm">
                <p className="text-yellow-200 text-sm mb-2">
                  <strong>Development Mode:</strong> Click the link below to reset your password:
                </p>
                <a
                  href={resetUrl}
                  className="text-white underline hover:text-yellow-300 transition-colors text-sm break-all"
                >
                  {resetUrl}
                </a>
              </div>
            )}

            {/* Instructions */}
            <div className="mb-8 text-center">
              <p className="text-blue-200 text-sm">
                If you don't see the email in your inbox, please check your spam folder.
              </p>
            </div>

            {/* Back to Sign In */}
            <button
              onClick={onBackToSignIn}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white py-3 rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300 flex items-center justify-center"
            >
              <ArrowLeftIcon className="w-5 h-5 mr-2" />
              Back to Sign In
            </button>

            {/* Footer */}
            <div className="text-center mt-6">
              <p className="text-xs text-blue-300">
                Secure • AI-Powered • Professional Valuations
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-800 flex items-center justify-center p-4">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 w-full max-w-md">
        {/* Glass Morphism Container */}
        <div className="backdrop-blur-lg bg-white/10 rounded-3xl p-8 shadow-2xl border border-white/20">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl mb-4 shadow-lg">
              <SparklesIcon className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">Forgot Password</h1>
            <p className="text-blue-200">Enter your email address and we'll send you a link to reset your password.</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Error Message */}
            {errors.root && (
              <div className="bg-red-500/20 border border-red-500/30 rounded-xl p-4 backdrop-blur-sm">
                <p className="text-red-200 text-sm">{errors.root.message}</p>
              </div>
            )}

            {/* Email Field */}
            <div className="space-y-2">
              <label htmlFor="email" className="text-white font-medium">
                Email Address
              </label>
              <div className="relative">
                <EnvelopeIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-blue-300" />
                <input
                  id="email"
                  type="email"
                  className={`w-full pl-11 pr-4 py-3 bg-white/10 border rounded-xl text-white placeholder-blue-200 backdrop-blur-sm transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent ${
                    errors.email ? 'border-red-400' : 'border-white/20'
                  }`}
                  placeholder="Enter your email address"
                  {...register('email', {
                    required: 'Email is required',
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: 'Invalid email address',
                    },
                  })}
                />
              </div>
              {errors.email && (
                <p className="text-red-300 text-sm">{errors.email.message}</p>
              )}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white py-3 rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Sending Reset Link...
                </div>
              ) : (
                'Send Reset Link'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="flex items-center my-6">
            <div className="flex-1 border-t border-white/20"></div>
            <span className="px-4 text-blue-200 text-sm">or</span>
            <div className="flex-1 border-t border-white/20"></div>
          </div>

          {/* Back to Sign In */}
          <div className="text-center">
            <button
              onClick={onBackToSignIn}
              className="text-white font-semibold hover:text-blue-300 transition-colors flex items-center justify-center w-full"
            >
              <ArrowLeftIcon className="w-4 h-4 mr-2" />
              Back to Sign In
            </button>
          </div>

          {/* Footer */}
          <div className="text-center mt-6">
            <p className="text-xs text-blue-300">
              Secure • AI-Powered • Professional Valuations
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

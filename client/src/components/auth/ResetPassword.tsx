import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { LockClosedIcon, SparklesIcon, EyeIcon, EyeSlashIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

interface ResetPasswordFormData {
  password: string;
  confirmPassword: string;
}

interface ResetPasswordProps {
  token: string;
  onSuccess: (authData: any) => void;
  onBackToSignIn: () => void;
}

export const ResetPassword: React.FC<ResetPasswordProps> = ({ token, onSuccess, onBackToSignIn }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isTokenValid, setIsTokenValid] = useState(true);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setError,
  } = useForm<ResetPasswordFormData>();

  const password = watch('password');

  useEffect(() => {
    // Validate token exists
    if (!token) {
      setIsTokenValid(false);
    }
  }, [token]);

  const onSubmit = async (data: ResetPasswordFormData) => {
    try {
      setIsLoading(true);
      
      const response = await fetch('http://localhost:5000/api/auth/reset-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token,
          password: data.password,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        onSuccess(result);
      } else {
        const errorData = await response.json();
        setError('root', {
          type: 'manual',
          message: errorData.error || 'Failed to reset password',
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

  if (!isTokenValid) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-900 via-pink-900 to-purple-800 flex items-center justify-center p-4">
        <div className="relative z-10 w-full max-w-md">
          <div className="backdrop-blur-lg bg-white/10 rounded-3xl p-8 shadow-2xl border border-white/20">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-red-500 to-pink-500 rounded-2xl mb-4 shadow-lg">
                <SparklesIcon className="w-8 h-8 text-white" />
              </div>
              <h1 className="text-3xl font-bold text-white mb-2">Invalid Link</h1>
              <p className="text-red-200 mb-6">This password reset link is invalid or has expired.</p>
              <button
                onClick={onBackToSignIn}
                className="w-full bg-gradient-to-r from-red-500 to-pink-500 text-white py-3 rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300"
              >
                Back to Sign In
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-900 via-teal-900 to-blue-800 flex items-center justify-center p-4">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-green-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-teal-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 w-full max-w-md">
        {/* Glass Morphism Container */}
        <div className="backdrop-blur-lg bg-white/10 rounded-3xl p-8 shadow-2xl border border-white/20">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-green-500 to-blue-500 rounded-2xl mb-4 shadow-lg">
              <LockClosedIcon className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">Reset Password</h1>
            <p className="text-green-200">Enter your new password below.</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Error Message */}
            {errors.root && (
              <div className="bg-red-500/20 border border-red-500/30 rounded-xl p-4 backdrop-blur-sm">
                <p className="text-red-200 text-sm">{errors.root.message}</p>
              </div>
            )}

            {/* Password Field */}
            <div className="space-y-2">
              <label htmlFor="password" className="text-white font-medium">
                New Password
              </label>
              <div className="relative">
                <LockClosedIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-green-300" />
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  className={`w-full pl-11 pr-12 py-3 bg-white/10 border rounded-xl text-white placeholder-green-200 backdrop-blur-sm transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent ${
                    errors.password ? 'border-red-400' : 'border-white/20'
                  }`}
                  placeholder="Create new password"
                  {...register('password', {
                    required: 'Password is required',
                    minLength: {
                      value: 8,
                      message: 'Password must be at least 8 characters',
                    },
                    pattern: {
                      value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
                      message: 'Password must contain at least one uppercase letter, one lowercase letter, and one number',
                    },
                  })}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-green-300 hover:text-white transition-colors"
                >
                  {showPassword ? (
                    <EyeSlashIcon className="w-5 h-5" />
                  ) : (
                    <EyeIcon className="w-5 h-5" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="text-red-300 text-sm">{errors.password.message}</p>
              )}
            </div>

            {/* Confirm Password Field */}
            <div className="space-y-2">
              <label htmlFor="confirmPassword" className="text-white font-medium">
                Confirm New Password
              </label>
              <div className="relative">
                <LockClosedIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-green-300" />
                <input
                  id="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  className={`w-full pl-11 pr-12 py-3 bg-white/10 border rounded-xl text-white placeholder-green-200 backdrop-blur-sm transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent ${
                    errors.confirmPassword ? 'border-red-400' : 'border-white/20'
                  }`}
                  placeholder="Confirm new password"
                  {...register('confirmPassword', {
                    required: 'Please confirm your password',
                    validate: (value) =>
                      value === password || 'Passwords do not match',
                  })}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-green-300 hover:text-white transition-colors"
                >
                  {showConfirmPassword ? (
                    <EyeSlashIcon className="w-5 h-5" />
                  ) : (
                    <EyeIcon className="w-5 h-5" />
                  )}
                </button>
              </div>
              {errors.confirmPassword && (
                <p className="text-red-300 text-sm">{errors.confirmPassword.message}</p>
              )}
            </div>

            {/* Password Requirements */}
            <div className="bg-blue-500/20 border border-blue-500/30 rounded-xl p-4 backdrop-blur-sm">
              <p className="text-blue-200 text-sm mb-2">Password must include:</p>
              <ul className="text-blue-200 text-sm space-y-1">
                <li className="flex items-center">
                  <CheckCircleIcon className="w-4 h-4 mr-2 text-green-400" />
                  At least 8 characters
                </li>
                <li className="flex items-center">
                  <CheckCircleIcon className="w-4 h-4 mr-2 text-green-400" />
                  One uppercase letter
                </li>
                <li className="flex items-center">
                  <CheckCircleIcon className="w-4 h-4 mr-2 text-green-400" />
                  One lowercase letter
                </li>
                <li className="flex items-center">
                  <CheckCircleIcon className="w-4 h-4 mr-2 text-green-400" />
                  One number
                </li>
              </ul>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-green-500 to-blue-500 text-white py-3 rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Resetting Password...
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <CheckCircleIcon className="w-5 h-5 mr-2" />
                  Reset Password
                </div>
              )}
            </button>
          </form>

          {/* Footer */}
          <div className="text-center mt-6">
            <p className="text-xs text-green-300">
              Secure • AI-Powered • Professional Valuations
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

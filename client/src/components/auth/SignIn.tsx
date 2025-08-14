import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { EyeIcon, EyeSlashIcon, SparklesIcon, EnvelopeIcon, LockClosedIcon } from '@heroicons/react/24/outline';

interface SignInFormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

interface SignInProps {
  onSwitchToSignUp: () => void;
  onSignIn: (data: { email: string; password: string }) => Promise<void>;
  onForgotPassword: () => void;
}

export const SignIn: React.FC<SignInProps> = ({ onSwitchToSignUp, onSignIn, onForgotPassword }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<SignInFormData>();

  const onSubmit = async (data: SignInFormData) => {
    try {
      setIsLoading(true);
      await onSignIn({
        email: data.email,
        password: data.password,
      });
    } catch (error: any) {
      setError('root', {
        type: 'manual',
        message: error.message || 'Invalid credentials. Please try again.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 flex items-center justify-center p-4">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 w-full max-w-md">
        {/* Glass Morphism Container */}
        <div className="backdrop-blur-lg bg-white/10 rounded-3xl p-8 shadow-2xl border border-white/20">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl mb-4 shadow-lg">
              <SparklesIcon className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
            <p className="text-purple-200">Sign in to your account to continue</p>
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
                <EnvelopeIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-purple-300" />
                <input
                  id="email"
                  type="email"
                  className={`w-full pl-11 pr-4 py-3 bg-white/10 border rounded-xl text-white placeholder-purple-200 backdrop-blur-sm transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent ${
                    errors.email ? 'border-red-400' : 'border-white/20'
                  }`}
                  placeholder="Enter your email"
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

            {/* Password Field */}
            <div className="space-y-2">
              <label htmlFor="password" className="text-white font-medium">
                Password
              </label>
              <div className="relative">
                <LockClosedIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-purple-300" />
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  className={`w-full pl-11 pr-12 py-3 bg-white/10 border rounded-xl text-white placeholder-purple-200 backdrop-blur-sm transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent ${
                    errors.password ? 'border-red-400' : 'border-white/20'
                  }`}
                  placeholder="Enter your password"
                  {...register('password', {
                    required: 'Password is required',
                    minLength: {
                      value: 6,
                      message: 'Password must be at least 6 characters',
                    },
                  })}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-purple-300 hover:text-white transition-colors"
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

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  className="rounded border-white/20 bg-white/10 text-purple-500 focus:ring-purple-400"
                  {...register('rememberMe')}
                />
                <span className="ml-2 text-sm text-purple-200">Remember me</span>
              </label>
              <button
                type="button"
                onClick={onForgotPassword}
                className="text-sm text-purple-300 hover:text-white transition-colors"
              >
                Forgot password?
              </button>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Signing In...
                </div>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="flex items-center my-6">
            <div className="flex-1 border-t border-white/20"></div>
            <span className="px-4 text-purple-200 text-sm">or</span>
            <div className="flex-1 border-t border-white/20"></div>
          </div>

          {/* Sign Up Link */}
          <div className="text-center">
            <p className="text-purple-200">
              Don't have an account?{' '}
              <button
                onClick={onSwitchToSignUp}
                className="text-white font-semibold hover:text-purple-300 transition-colors"
              >
                Sign up for free
              </button>
            </p>
          </div>

          {/* Footer */}
          <div className="text-center mt-6">
            <p className="text-xs text-purple-300">
              Secure • AI-Powered • Professional Valuations
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

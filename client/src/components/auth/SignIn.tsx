import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { EyeIcon, EyeSlashIcon, EnvelopeIcon, PhoneIcon, LockClosedIcon } from '@heroicons/react/24/outline';

interface SignInFormData {
  emailOrPhone: string;
  password: string;
  rememberMe: boolean;
}

interface SignInProps {
  onSwitchToSignUp: () => void;
  onSignIn: (data: SignInFormData) => Promise<void>;
}

export const SignIn: React.FC<SignInProps> = ({ onSwitchToSignUp, onSignIn }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [inputType, setInputType] = useState<'email' | 'phone'>('email');
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch
  } = useForm<SignInFormData>();

  const emailOrPhone = watch('emailOrPhone', '');

  // Auto-detect if input is email or phone
  React.useEffect(() => {
    if (emailOrPhone) {
      const isEmail = emailOrPhone.includes('@');
      const isPhone = /^\+?[\d\s-()]+$/.test(emailOrPhone);
      
      if (isEmail) {
        setInputType('email');
      } else if (isPhone) {
        setInputType('phone');
      }
    }
  }, [emailOrPhone]);

  const onSubmit = async (data: SignInFormData) => {
    setIsLoading(true);
    try {
      await onSignIn(data);
    } catch (error) {
      console.error('Sign in error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-blue-100">
            <span className="text-2xl font-bold text-blue-600">V</span>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to ValuAI
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Access your UCaaS valuation dashboard
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="space-y-4">
            <div>
              <label htmlFor="emailOrPhone" className="sr-only">
                Email address or phone number
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  {inputType === 'email' ? (
                    <EnvelopeIcon className="h-5 w-5 text-gray-400" />
                  ) : (
                    <PhoneIcon className="h-5 w-5 text-gray-400" />
                  )}
                </div>
                <input
                  {...register('emailOrPhone', {
                    required: 'Email or phone number is required',
                    validate: (value) => {
                      const isEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
                      const isPhone = /^\+?[\d\s-()]{10,}$/.test(value.replace(/\s/g, ''));
                      
                      if (!isEmail && !isPhone) {
                        return 'Please enter a valid email address or phone number';
                      }
                      return true;
                    }
                  })}
                  type="text"
                  autoComplete="username"
                  className="appearance-none rounded-md relative block w-full px-3 py-2 pl-10 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                  placeholder="Email address or phone number"
                />
              </div>
              {errors.emailOrPhone && (
                <p className="mt-1 text-sm text-red-600">{errors.emailOrPhone.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LockClosedIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register('password', {
                    required: 'Password is required',
                    minLength: {
                      value: 6,
                      message: 'Password must be at least 6 characters'
                    }
                  })}
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  className="appearance-none rounded-md relative block w-full px-3 py-2 pl-10 pr-10 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                  placeholder="Password"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
              )}
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                {...register('rememberMe')}
                id="remember-me"
                name="remember-me"
                type="checkbox"
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                Remember me
              </label>
            </div>

            <div className="text-sm">
              <a href="#" className="font-medium text-blue-600 hover:text-blue-500">
                Forgot your password?
              </a>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                'Sign in'
              )}
            </button>
          </div>

          <div className="text-center">
            <span className="text-sm text-gray-600">
              Don't have an account?{' '}
              <button
                type="button"
                onClick={onSwitchToSignUp}
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                Sign up
              </button>
            </span>
          </div>
        </form>
      </div>
    </div>
  );
};

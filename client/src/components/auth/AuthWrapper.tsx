import React, { useState } from 'react';
import { SignIn } from './SignIn';
import { SignUp } from './SignUp';
import { ForgotPassword } from './ForgotPassword';
import { ResetPassword } from './ResetPassword';

interface AuthWrapperProps {
  onAuthSuccess: (authData: any) => void;
}

export const AuthWrapper: React.FC<AuthWrapperProps> = ({ onAuthSuccess }) => {
  const [currentView, setCurrentView] = useState<'signin' | 'signup' | 'forgot' | 'reset'>('signin');
  const [resetToken, setResetToken] = useState<string>('');

  const handleSignIn = async (data: any) => {
    try {
      console.log('Frontend signin data:', data);  // Debug logging
      
      // Transform data to match backend expectations
      const signinData = {
        emailOrPhone: data.email,
        password: data.password
      };
      
      console.log('Transformed signin data:', signinData);  // Debug logging
      
      // Here you would integrate with your authentication API
      const response = await fetch('http://localhost:5000/api/auth/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(signinData),
      });

      console.log('Signin response status:', response.status);  // Debug logging

      if (response.ok) {
        const authData = await response.json();
        console.log('Signin successful:', authData);  // Debug logging
        onAuthSuccess(authData);
      } else {
        const errorData = await response.json();
        console.error('Signin error response:', errorData);  // Debug logging
        throw new Error(errorData.error || 'Authentication failed');
      }
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const handleSignUp = async (data: any) => {
    try {
      console.log('Frontend signup data:', data);  // Debug logging
      
      // Transform data to match backend expectations
      const signupData = {
        firstName: data.firstName,
        lastName: data.lastName,
        emailOrPhone: data.emailOrPhone,
        password: data.password
      };
      
      console.log('Transformed signup data:', signupData);  // Debug logging
      
      // Here you would integrate with your authentication API
      const response = await fetch('http://localhost:5000/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(signupData),
      });

      console.log('Signup response status:', response.status);  // Debug logging

      if (response.ok) {
        const authData = await response.json();
        console.log('Signup successful:', authData);  // Debug logging
        onAuthSuccess(authData);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Registration failed');
      }
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  const handleResetSuccess = (authData: any) => {
    console.log('Password reset successful:', authData);
    onAuthSuccess(authData);
  };

  // Check for reset token in URL
  React.useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
      setResetToken(token);
      setCurrentView('reset');
    }
  }, []);

  if (currentView === 'reset') {
    return (
      <ResetPassword
        token={resetToken}
        onSuccess={handleResetSuccess}
        onBackToSignIn={() => {
          setCurrentView('signin');
          setResetToken('');
          // Clear URL params
          window.history.replaceState({}, document.title, window.location.pathname);
        }}
      />
    );
  }

  if (currentView === 'forgot') {
    return (
      <ForgotPassword
        onBackToSignIn={() => setCurrentView('signin')}
      />
    );
  }

  if (currentView === 'signup') {
    return (
      <SignUp
        onSignUp={handleSignUp}
        onSwitchToSignIn={() => setCurrentView('signin')}
      />
    );
  }

  return (
    <SignIn
      onSignIn={handleSignIn}
      onSwitchToSignUp={() => setCurrentView('signup')}
      onForgotPassword={() => setCurrentView('forgot')}
    />
  );
};

import React, { useState } from 'react';
import { SignIn } from './SignIn';
import { SignUp } from './SignUp';

interface AuthWrapperProps {
  onAuthSuccess: (user: any) => void;
}

export const AuthWrapper: React.FC<AuthWrapperProps> = ({ onAuthSuccess }) => {
  const [isSignUp, setIsSignUp] = useState(false);

  const handleSignIn = async (data: any) => {
    try {
      console.log('Frontend signin data:', data);  // Debug logging
      
      // Here you would integrate with your authentication API
      const response = await fetch('http://localhost:5000/api/auth/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
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
      
      // Here you would integrate with your authentication API
      const response = await fetch('http://localhost:5000/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
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

  return (
    <>
      {isSignUp ? (
        <SignUp
          onSignUp={handleSignUp}
          onSwitchToSignIn={() => setIsSignUp(false)}
        />
      ) : (
        <SignIn
          onSignIn={handleSignIn}
          onSwitchToSignUp={() => setIsSignUp(true)}
        />
      )}
    </>
  );
};

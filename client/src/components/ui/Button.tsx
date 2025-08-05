import React from 'react';

interface ButtonProps {
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  variant?: 'primary' | 'secondary' | 'success' | 'danger';
  className?: string;
  disabled?: boolean;
  children: React.ReactNode;
}

const getVariantClasses = (variant: string): string => {
  switch (variant) {
    case 'primary':
      return 'bg-blue-500 hover:bg-blue-600 text-white';
    case 'secondary':
      return 'bg-gray-500 hover:bg-gray-600 text-white';
    case 'success':
      return 'bg-green-500 hover:bg-green-600 text-white';
    case 'danger':
      return 'bg-red-500 hover:bg-red-600 text-white';
    default:
      return 'bg-blue-500 hover:bg-blue-600 text-white';
  }
};

export const Button: React.FC<ButtonProps> = ({
  onClick,
  type = 'button',
  variant = 'primary',
  className = '',
  disabled = false,
  children
}) => {
  const baseClasses = 'px-4 py-2 rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-offset-2';
  const variantClasses = getVariantClasses(variant);
  const disabledClasses = disabled ? 'opacity-50 cursor-not-allowed' : '';
  
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses} ${disabledClasses} ${className}`}
    >
      {children}
    </button>
  );
};

import React from 'react';
import { SparklesIcon, CalculatorIcon, ChartBarIcon } from '@heroicons/react/24/outline';

interface FeatureCardProps {
  title?: string;
  description?: string;
  icon?: 'sparkles' | 'calculator' | 'chart';
  gradient?: string;
}

const iconMap = {
  sparkles: SparklesIcon,
  calculator: CalculatorIcon,
  chart: ChartBarIcon,
};

export const FeatureCard: React.FC<FeatureCardProps> = ({
  title = 'Feature Title',
  description = 'Feature description goes here',
  icon = 'sparkles',
  gradient = 'from-blue-600 to-purple-600'
}) => {
  const IconComponent = iconMap[icon];

  return (
    <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6 hover:shadow-2xl transition-all duration-300">
      <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${gradient} flex items-center justify-center mb-4`}>
        <IconComponent className="w-6 h-6 text-white" />
      </div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
};

interface HeroSectionProps {
  title?: string;
  subtitle?: string;
  ctaText?: string;
  backgroundGradient?: string;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  title = 'Welcome to ValuAI',
  subtitle = 'AI-Powered UCaaS Valuation Platform',
  ctaText = 'Get Started',
  backgroundGradient = 'from-blue-50 via-indigo-50 to-purple-50'
}) => {
  return (
    <div className={`min-h-[60vh] flex items-center justify-center bg-gradient-to-br ${backgroundGradient} relative overflow-hidden`}>
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-32 w-80 h-80 rounded-full bg-gradient-to-br from-blue-400/20 to-purple-600/20 blur-3xl"></div>
        <div className="absolute -bottom-40 -left-32 w-80 h-80 rounded-full bg-gradient-to-br from-indigo-400/20 to-blue-600/20 blur-3xl"></div>
      </div>
      
      <div className="text-center relative z-10 max-w-4xl mx-auto px-4">
        <h1 className="text-6xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 bg-clip-text text-transparent mb-6">
          {title}
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          {subtitle}
        </p>
        <button className="btn-modern-primary px-8 py-4 text-lg">
          {ctaText}
        </button>
      </div>
    </div>
  );
};

export default { FeatureCard, HeroSection };

# Azure-specific configuration for Flask app
import os
from datetime import timedelta

class AzureConfig:
    """Azure production configuration"""
    
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'azure-production-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'azure-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///valuai.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'sslmode': 'require'
        } if DATABASE_URL and 'postgres' in DATABASE_URL else {}
    }
    
    # Azure-specific settings
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    APPLICATION_INSIGHTS_INSTRUMENTATION_KEY = os.environ.get('APPINSIGHTS_INSTRUMENTATIONKEY')
    
    # OpenAI configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # CORS configuration for Azure
    CORS_ORIGINS = [
        'https://valuai-frontend-dev.azurewebsites.net',
        'https://valuai-frontend-staging.azurewebsites.net',
        'https://valuai-frontend.azurewebsites.net',
        'https://valuai.com',  # Add your custom domain
    ]
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = '/tmp/uploads'  # Azure App Service temp directory
    
    # Logging configuration
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')
    
    # Security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
    }
    
    # Cache configuration (Redis if available)
    CACHE_TYPE = 'simple'  # Use Redis in production
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Session configuration
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

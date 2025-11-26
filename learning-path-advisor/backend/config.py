"""
Configuration management for Learning Path Advisor API
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    DEFAULT_PATHFINDING_ALGORITHM = os.getenv('DEFAULT_PATHFINDING_ALGORITHM', 'dijkstra')
    DEFAULT_DECISION_STRATEGY = os.getenv('DEFAULT_DECISION_STRATEGY', 'meu')
    DEFAULT_LEARNING_STYLE = os.getenv('DEFAULT_LEARNING_STYLE', 'balanced')
    
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_DEFAULT = os.getenv('RATE_LIMIT_DEFAULT', '100 per hour')
    RATE_LIMIT_STORAGE_URL = os.getenv('RATE_LIMIT_STORAGE_URL', 'memory://')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    RATE_LIMIT_ENABLED = False

config_name = os.getenv('FLASK_ENV', 'development')
if config_name == 'production':
    config = ProductionConfig()
elif config_name == 'testing':
    config = TestingConfig()
else:
    config = DevelopmentConfig()
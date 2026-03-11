import os

class Config:
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    
    API_BASE_URL = os.environ.get('API_BASE_URL', 'http://example.com/api')
    API_TIMEOUT = int(os.environ.get('API_TIMEOUT', '30'))
    MAX_CONCURRENT_REQUESTS = int(os.environ.get('MAX_CONCURRENT_REQUESTS', '5'))
    
    DATA_CONFIG_PATH = os.environ.get('DATA_CONFIG_PATH', 'config/data.json')

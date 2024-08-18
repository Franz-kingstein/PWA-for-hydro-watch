```python
import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///default.db'
    FIREBASE_CERT_PATH = os.environ.get('FIREBASE_CERT_PATH') or 'path/to/your/firebase-adminsdk.json'
    FIREBASE_DATABASE_URL = os.environ.get('FIREBASE_DATABASE_URL') or 'https://your-database-url.firebaseio.com/'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///dev.db'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///test.db'

class ProductionConfig(Config):
    """Production configuration."""
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql://

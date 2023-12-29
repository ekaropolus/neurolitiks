import os
from dotenv import load_dotenv

# Load environment variables from .env file
project_folder = os.path.expanduser('~/mysite')  # Adjust the path as needed
load_dotenv(os.path.join(project_folder, '.env'))

# Access environment variables
URI_MONGO = os.environ.get("URI_MONGO")

class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = True



import os
from dotenv import load_dotenv

# Load environment variables from .env file
project_folder = os.path.expanduser('~/mysite')  # Adjust the path as needed
load_dotenv(os.path.join(project_folder, '.env'))

# Access environment variables
CLARIFAI_PAT = os.environ.get("CLARIFAI_PAT")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")

# Global dictionary to store responses
policies = {}
import os
from dotenv import load_dotenv

# Load environment variables from .env file
project_folder = os.path.expanduser('~/mysite')  # Adjust the path as needed
load_dotenv(os.path.join(project_folder, '.env'))

# Now you can access the environment variables
EAI_USERNAME = os.getenv("EAI_USERNAME")
EAI_PASSWORD = os.getenv("EAI_PASSWORD")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")



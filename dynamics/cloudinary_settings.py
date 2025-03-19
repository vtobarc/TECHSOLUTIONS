# cloudinary_settings.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Explicit configuration
CLOUDINARY_CLOUD_NAME = 'intitulado'  # Hardcoded from your env vars
CLOUDINARY_API_KEY = '844554634418234'  # Hardcoded from your env vars
CLOUDINARY_API_SECRET = 'FSn6G0MfhIWiyanNcOwvo1bEYF8'  # Hardcoded from your env vars

# Configure the dictionary that cloudinary_storage expects
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
}


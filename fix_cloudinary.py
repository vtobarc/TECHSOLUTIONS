# Add this to your settings.py file
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'dshj58ucs'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', '241739348942567'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', 'wWcQab-9C_R0poTu8p5aOaAhvSk'),

}


# Make sure this comes after the CLOUDINARY_STORAGE dictionary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# You can also configure Cloudinary directly
import cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)




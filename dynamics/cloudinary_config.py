import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

# CRITICAL: Use your actual Cloudinary cloud name
CLOUDINARY_CLOUD_NAME = 'dshj58ucs'  # Your correct cloud name
CLOUDINARY_API_KEY = '241739348942567'  # Replace with your actual API key
CLOUDINARY_API_SECRET = 'wWcQab-9C_R0poTu8p5aOaAhvSk'  # Replace with your actual API secret

# Set environment variables directly (some libraries check these)
os.environ['CLOUDINARY_CLOUD_NAME'] = CLOUDINARY_CLOUD_NAME
os.environ['CLOUDINARY_API_KEY'] = CLOUDINARY_API_KEY
os.environ['CLOUDINARY_API_SECRET'] = CLOUDINARY_API_SECRET
os.environ['CLOUDINARY_URL'] = f'cloudinary://{CLOUDINARY_API_KEY}:{CLOUDINARY_API_SECRET}@{CLOUDINARY_CLOUD_NAME}'

# Configure cloudinary directly
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# Export the configuration dictionary for Django Cloudinary Storage
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
}


import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

# IMPORTANT: Cloudinary cloud names are case-sensitive and should be lowercase
CLOUDINARY_CLOUD_NAME = 'intitulado'  # Make sure this is lowercase
CLOUDINARY_API_KEY = '844554634418234'
CLOUDINARY_API_SECRET = 'FSn6G0MfhIWiyanNcOwvo1bEYF8'

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

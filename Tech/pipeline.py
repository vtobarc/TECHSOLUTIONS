# dynamics/pipeline.py

def save_profile(backend, user, response, *args, **kwargs):
    """
    Pipeline function to save additional user data from social auth
    """
    if backend.name == 'google-oauth2':
        if response.get('email'):
            user.email = response['email']
        
    elif backend.name == 'facebook':
        if response.get('email'):
            user.email = response['email']
    
    elif backend.name == 'linkedin-oauth2':
        if response.get('emailAddress'):
            user.email = response['emailAddress']
    
    # Set default role if needed
    if hasattr(user, 'rol') and not user.rol:
        user.rol = 'Cliente'  # Default role
    
    # Handle IP address like in your login signal
    if 'request' in kwargs:
        request = kwargs['request']
        ip = request.META.get('REMOTE_ADDR', None)
        if ip and hasattr(user, 'ip_registro'):
            user.ip_registro = ip
    
    user.save()
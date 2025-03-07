# dynamics/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si el usuario está autenticado y ha iniciado sesión
        if request.user.is_authenticated:
            # Si el usuario es admin, redirigir al admin_dashboard
            if hasattr(request.user, 'rol') and request.user.rol == 'Admin':
                if request.path == reverse('login'):
                    return redirect('admin_dashboard')  # Redirigir a admin dashboard
            else:
                # Si no es admin, redirigir a la página de cliente
                if request.path == reverse('login'):
                    return redirect('cliente_home')  # Redirigir a la página del cliente
        response = self.get_response(request)
        return response

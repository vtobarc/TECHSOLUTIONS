# myapp/context_processors.py

from .models import Company  # O ajusta esto según el modelo que estés usando para la empresa

def company_info(request):
    company = Company.objects.first()  # O ajusta según cómo obtienes la empresa
    return {'company': company}

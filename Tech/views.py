from cProfile import Profile
from decimal import Decimal
import os
import json
import csv
from PIL import Image
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from .models import Sale
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import  CategoryForm, CertificationForm, CompanyForm, CustomUserCreationForm  # Importa el formulario personalizado
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from .models import Company, CustomUser, Education, Experience, OrderItem, PaymentMethod, Quote, QuoteItem, Sale, SaleItem, User
from .forms import ProfileForm, EducationForm, ExperienceForm, PaymentMethodForm
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.utils.timesince import timesince
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from .models import Order
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Product, Category, StockMovement
from .forms import ProductForm, StockMovementForm
from datetime import datetime, timezone, timedelta
from django.db.models import Count, Sum, F
from .models import Category
from django.db import transaction
from django.db.models import Q
from django.db.models.functions import TruncDate
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.contrib import messages
from .models import Product  # Asegúrate de importar tu modelo de productos
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import Quote
import json
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from django.contrib.auth.decorators import user_passes_test
from django.core.files.base import File

# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.urls import reverse
from django.template.loader import render_to_string
from django.db import models  # Importa models.F correctamente
from django.http import HttpResponseForbidden
from .models import Order, OrderItem, Product

# Reportes
import xlsxwriter
from io import BytesIO, StringIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
# Utilidades
from datetime import datetime, timedelta
import json
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, F
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import (
    CustomUser, Product, Category, Sale, SaleItem, 
    StockMovement, Company, Certification, Quote
)
from .forms import (
    ProductForm, CategoryForm, CompanyForm, CertificationForm,
    CustomUserCreationForm
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.forms import inlineformset_factory
from .models import Product, ProductImage
from .forms import ProductForm, ProductImageForm

# Create ProductImage formset
ProductImageFormSet = inlineformset_factory(
    Product, 
    ProductImage,
    form=ProductImageForm,
    extra=3,  # Number of empty forms to display
    max_num=10,  # Maximum number of forms/images
    validate_max=True,  # Enforce max_num
    can_delete=True
)


def is_admin(user):
    return user.is_authenticated and hasattr(user, 'rol') and user.rol == 'Admin'



# Vista para la página principal
def index(request):
    return HttpResponse("home/index.html")
    
def home_view(request):
    company = Company.objects.first()  # Puedes cambiar la lógica si necesitas obtener una empresa específica
    categorias = Category.objects.all()
    productos_por_categoria = {}
    all_certifications = Certification.objects.all()

    # Obtener los empleados de la empresa
    employees = company.employees.all() if company else []

    # Iterar sobre las categorías y obtener un producto al azar de cada una
    for categoria in categorias:
        producto_aleatorio = Product.objects.filter(category=categoria, is_available=True).order_by('?').first()
        if producto_aleatorio:
            productos_por_categoria[categoria] = [producto_aleatorio]

    destacados = Product.objects.filter(is_available=True).order_by('-created_at')[:10]  # Últimos 10 agregados
    mas_vendidos = Product.objects.filter(is_available=True).annotate(
        total_vendido=models.Sum('saleitem__quantity')
    ).order_by('-total_vendido')[:10]  # Top 10 más vendidos

    contexto = {
        'company': company,
        'employees': employees,  # Agregar empleados al contexto
        'destacados': destacados,
        'mas_vendidos': mas_vendidos,
        'productos_por_categoria': productos_por_categoria,
        'certifications': all_certifications,  # Pasar todas las certificaciones

    }

    return render(request, 'home/index.html', contexto)



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Incluir files para imágenes
        if form.is_valid():
            user = form.save()

            # Especificamos el backend de autenticación aquí
            backend = 'django.contrib.auth.backends.ModelBackend'  # Asegúrate de que sea el backend correcto
            login(request, user, backend=backend)  # Inicia sesión automáticamente después del registro

            messages.success(request, 'Te has registrado correctamente.')  # Mensaje de éxito
            return redirect('cliente_home')  # Redirige a la página de inicio
        else:
            messages.error(request, 'Por favor, corrige los errores abajo.')  # Mensaje de error
    else:
        form = CustomUserCreationForm()

    return render(request, 'login_and_signup/signup.html', {'form': form})

from django.contrib import messages


def user_login(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(user.rol)  # Para verificar el valor del rol

            login(request, user)
            messages.success(request, "¡Inicio de sesión exitoso!")
            
            # Verifica si el rol es 'Admin' y redirige al dashboard correspondiente
            if user.rol == 'Admin':
                return redirect('admin_dashboard')

            # Si no es admin, redirige a la página principal
            return redirect('home_view')
        else:
            messages.error(request, "Credenciales inválidas. Por favor, intenta nuevamente.")
    
    return render(request, 'login_and_signup/login.html')




from django.contrib.auth import logout
def custom_logout(request):
    if request.method == "POST":
        logout(request)  # Cierra la sesión
        request.session.flush()  # Limpia cualquier dato de sesión adicional
        messages.success(request, "Has cerrado sesión exitosamente.")
        return redirect('user_login')  # Redirige a la página de inicio de sesión
    else:
        return redirect('home_view')  # Redirige a la página principal en caso de GET (o si no es POST)



@receiver(user_logged_in)
def update_user_login_info(sender, request, user, **kwargs):
    # Obtener la IP del request
    ip = request.META.get('REMOTE_ADDR', None)  # REMOTE_ADDR contiene la IP del cliente
    if ip:
        user.ip_registro = ip  # Guardar la IP en el modelo
        user.last_login_time = now()  # Actualizar la última vez que inició sesión
        user.save()

@receiver(user_logged_in)
def update_last_login_time(sender, request, user, **kwargs):
    user.last_login_time = user.last_login
    user.save()
from django.contrib import messages

@login_required
def perfil(request):
    user = request.user
    education = Education.objects.filter(user=user)
    experience = Experience.objects.filter(user=user)
    payment_methods = PaymentMethod.objects.filter(user=user)
    habilidades_tecnicas = user.habilidades_tecnicas.split(",") if user.habilidades_tecnicas else []
    habilidades_blandas = user.habilidades_blandas.split(",") if user.habilidades_blandas else []
    
    # Añadimos la información extra que se necesita mostrar
    last_login_time = user.last_login_time
    ip_registro = user.ip_registro or "None"  # Si no tiene IP, mostramos "None"
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')  # Redirigir a la misma página o a la que desees
        else:
            messages.error(request, 'Hubo un error al actualizar el perfil.')
    else:
        form = ProfileForm(instance=user)

    context = {
        'form': form,
        'education': education,
        'experience': experience,
        'payment_methods': payment_methods,
        'habilidades_tecnicas': habilidades_tecnicas,
        'habilidades_blandas': habilidades_blandas,
        'last_login_time': last_login_time,
        'ip_registro': ip_registro
    }
    return render(request, 'profile/profile.html', context)
@login_required
def profile_view(request):
    user = request.user
    
    education = Education.objects.filter(user=user)
    experience = Experience.objects.filter(user=user)
    habilidades_tecnicas = user.habilidades_tecnicas.split(',') if user.habilidades_tecnicas else []
    habilidades_blandas = user.habilidades_blandas.split(',') if user.habilidades_blandas else []

    return render(request, 'profile/profile_publico.html', {
        'user': user,
         'education': education,
        'experience': experience,
        'habilidades_tecnicas': habilidades_tecnicas,
        'habilidades_blandas': habilidades_blandas,
    })

@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('foto_perfil'):
        request.user.foto_perfil = request.FILES['foto_perfil']
        request.user.save()
        return JsonResponse({'success': True, 'url': request.user.foto_perfil.url})
    return JsonResponse({'success': False})

@login_required
def update_cover_photo(request):
    if request.method == 'POST' and request.FILES.get('cover_photo'):
        request.user.cover_photo = request.FILES['cover_photo']
        request.user.save()
        return JsonResponse({'success': True, 'url': request.user.cover_photo.url})
    return JsonResponse({'success': False})

@login_required
def update_profile_field(request):
    if request.method == 'POST':
        field = request.POST.get('field')
        value = request.POST.get('value')
        if hasattr(request.user, field):
            setattr(request.user, field, value)
            request.user.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return JsonResponse({'success': True, 'id': education.id})
    return JsonResponse({'success': False})

@login_required
def update_education(request, education_id):
    education = Education.objects.get(id=education_id, user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def delete_education(request, education_id):
    if request.method == 'POST':
        education = Education.objects.get(id=education_id, user=request.user)
        education.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return JsonResponse({'success': True, 'id': experience.id})
    return JsonResponse({'success': False})

@login_required
def update_experience(request, experience_id):
    experience = Experience.objects.get(id=experience_id, user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def delete_experience(request, experience_id):
    if request.method == 'POST':
        experience = Experience.objects.get(id=experience_id, user=request.user)
        experience.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def add_payment_method(request):
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.user = request.user
            payment_method.save()
            return JsonResponse({'success': True, 'id': payment_method.id})
    return JsonResponse({'success': False})

@login_required
def update_payment_method(request, payment_method_id):
    payment_method = PaymentMethod.objects.get(id=payment_method_id, user=request.user)
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=payment_method)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def delete_payment_method(request, payment_method_id):
    if request.method == 'POST':
        payment_method = PaymentMethod.objects.get(id=payment_method_id, user=request.user)
        payment_method.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def update_dark_mode(request):
    if request.method == 'POST':
        dark_mode = request.POST.get('dark_mode') == 'true'
        request.user.dark_mode = dark_mode
        request.user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def update_notification_settings(request):
    if request.method == 'POST':
        email_notifications = request.POST.get('email_notifications') == 'true'
        push_notifications = request.POST.get('push_notifications') == 'true'
        notification_settings = request.user.notification_settings
        notification_settings.email_notifications = email_notifications
        notification_settings.push_notifications = push_notifications
        notification_settings.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def nosotros_view(request):
    company = Company.objects.first()  
    categorias = Category.objects.all()
    productos_por_categoria = {}
    all_certifications = Certification.objects.all()
    # Si existe company.values, hacer el split
    values_list = company.values.split(',') if company and company.values else []
    # Obtener los empleados de la empresa
    employees = company.employees.all() if company else []
    # Iterar sobre las categorías y obtener un producto al azar de cada una
    for categoria in categorias:
        producto_aleatorio = Product.objects.filter(category=categoria, is_available=True).order_by('?').first()
        if producto_aleatorio:
            productos_por_categoria[categoria] = [producto_aleatorio]

    destacados = Product.objects.filter(is_available=True).order_by('-created_at')[:10]  # Últimos 10 agregados
    mas_vendidos = Product.objects.filter(is_available=True).annotate(
        total_vendido=models.Sum('saleitem__quantity')
    ).order_by('-total_vendido')[:10]  # Top 10 más vendidos

    contexto = {
        'company': company,
        'employees': employees,  # Agregar empleados al contexto
        'destacados': destacados,
        'mas_vendidos': mas_vendidos,
        'productos_por_categoria': productos_por_categoria,
        'certifications': all_certifications,  # Pasar todas las certificaciones
        'values_list': values_list,


    }

    return render(request, 'dashboard/nosotros.html', contexto)



@login_required
def servicios(request):
    return redirect('dashboard')  # Redirige automáticamente a la vista de dashboard

@login_required
def dashboard(request):
    # Total de productos
    total_products = Product.objects.filter(is_available=True).count()

    # Productos con stock bajo
    low_stock_products = Product.objects.filter(is_available=True, stock__lte=models.F('minimum_stock')).count()

    # Valor total del inventario (solo productos disponibles)
    total_value = sum(product.stock * product.price for product in Product.objects.filter(is_available=True))

    # Obtener los productos recientes
    recent_products = Product.objects.filter(is_available=True).order_by('-updated_at')[:5]

    # Productos con stock bajo (para la tabla)
    low_stock = Product.objects.filter(is_available=True, stock__lte=models.F('minimum_stock'))

    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'total_value': total_value,
        'recent_products': recent_products,
        'low_stock': low_stock,
    }
    
    return render(request, 'inventory/dashboard.html', context)



@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_available=True)  # Solo permitir acceso a productos disponibles
    return render(request, 'inventory/product_detail.html', {'product': product})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar el producto primero sin generar códigos
                    product = form.save()
                    
                    # Ahora guardar las imágenes
                    formset.instance = product
                    instances = formset.save(commit=False)
                    
                    for instance in instances:
                        instance.product = product
                        instance.save()
                    
                    # Procesar eliminaciones
                    for obj in formset.deleted_objects:
                        obj.delete()
                    
                    # Asegurarse de que haya una imagen principal
                    if not product.images.filter(is_main=True).exists() and product.images.exists():
                        first_image = product.images.first()
                        first_image.is_main = True
                        first_image.save()
                    
                    messages.success(request, 'Producto agregado exitosamente.')
                    return redirect('product_list')
                    
            except IntegrityError as e:
                logger.error(f"Error al crear producto: {str(e)}")
                messages.error(request, f'Error: {str(e)}. Inténtelo de nuevo.')
            except Exception as e:
                logger.error(f"Error inesperado al crear producto: {str(e)}")
                messages.error(request, f'Error inesperado: {str(e)}. Inténtelo de nuevo.')
    else:
        form = ProductForm()
        formset = ProductImageFormSet()

    return render(request, 'inventory/product_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Agregar Producto'
    })

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar el producto
                    product = form.save()
                    
                    # Guardar las imágenes
                    instances = formset.save(commit=False)
                    for instance in instances:
                        instance.product = product
                        instance.save()
                    
                    # Procesar eliminaciones
                    for obj in formset.deleted_objects:
                        obj.delete()
                    
                    # Asegurarse de que haya una imagen principal
                    if not product.images.filter(is_main=True).exists() and product.images.exists():
                        first_image = product.images.first()
                        first_image.is_main = True
                        first_image.save()
                    
                    messages.success(request, 'Producto actualizado exitosamente.')
                    return redirect('product_list')
                    
            except Exception as e:
                logger.error(f"Error al actualizar producto: {str(e)}")
                messages.error(request, f'Error al actualizar el producto: {str(e)}')
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)

    return render(request, 'inventory/product_form.html', {
        'form': form,
        'formset': formset,
        'product': product,
        'title': 'Editar Producto'
    })

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Eliminar las imágenes asociadas
                product.images.all().delete()
                # Marcar el producto como no disponible
                product.is_available = False
                product.save()
                
                messages.success(request, 'Producto marcado como no disponible exitosamente.')
                return redirect('product_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar el producto: {str(e)}')
            return redirect('product_list')
            
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})

# Vista adicional para manejar la eliminación de imágenes individuales vía AJAX
@login_required
def delete_product_image(request, image_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            image = get_object_or_404(ProductImage, id=image_id)
            was_main = image.is_main
            product = image.product
            
            # Eliminar la imagen
            image.delete()
            
            # Si era la imagen principal, establecer otra como principal
            if was_main and product.images.exists():
                new_main = product.images.first()
                new_main.is_main = True
                new_main.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

# Vista adicional para establecer una imagen como principal
@login_required
def set_main_image(request, image_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            image = get_object_or_404(ProductImage, id=image_id)
            product = image.product
            
            # Quitar la marca de principal de todas las imágenes del producto
            product.images.update(is_main=False)
            
            # Establecer la imagen seleccionada como principal
            image.is_main = True
            image.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@login_required
def export_products(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventory_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Código', 'Nombre', 'Categoría', 'Stock', 'Precio', 'Valor Total'])
    
    # Solo productos disponibles
    products = Product.objects.filter(is_available=True)
    for product in products:
        writer.writerow([
            product.code,
            product.name,
            product.category.name if product.category else '',
            product.stock,
            product.price,
            product.stock * product.price
        ])
    
    return response


@login_required
def print_labels(request):
    # Solo productos disponibles
    products = Product.objects.filter(is_available=True)
    return render(request, 'inventory/print_labels.html', {'products': products})

@login_required
def category_list(request):
    categories = Category.objects.annotate(
        product_count=Count('product', filter=Q(product__is_available=True)),  # Filtrar productos disponibles
        total_stock=Sum('product__stock', filter=Q(product__is_available=True)),  # Filtrar productos disponibles
        total_value=Sum(F('product__stock') * F('product__price'), filter=Q(product__is_available=True))  # Solo productos disponibles
    )
    return render(request, 'inventory/category_list.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'inventory/category_form.html', {'form': form})
# inventory/views.py (Agregar la vista de edición)
@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'inventory/category_form.html', {
        'form': form,
        'category': category
    })



@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # Buscar o crear la categoría "Sin Categoría"
    uncategorized, created = Category.objects.get_or_create(name="Sin Categoría", defaults={"description": "Productos sin categoría asignada"})

    if request.method == "POST":
        # Mover productos a la categoría "Sin Categoría"
        Product.objects.filter(category=category).update(category=uncategorized)

        # Eliminar la categoría
        category.delete()
        messages.success(request, "Categoría eliminada. Los productos se movieron a 'Sin Categoría'.")

        return redirect("category_list")

    return render(request, "inventory/category_confirm_delete.html", {"category": category})


@login_required
def reports(request):
    # Obtener el rango de fechas (último mes por defecto)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    # Estadísticas generales (solo productos disponibles)
    total_products = Product.objects.filter(is_available=True).count()
    total_stock = Product.objects.filter(is_available=True).aggregate(total=Sum('stock'))['total'] or 0
    total_value = Product.objects.filter(is_available=True).aggregate(
        total=Sum(F('stock') * F('price'))
    )['total'] or 0
    
    # Estadísticas de ventas
  
    total_sales = SaleItem.objects.filter(
    sale__date__range=[start_date, end_date],
    product__is_available=True
    ).count()

    total_revenue = SaleItem.objects.filter(
    sale__date__range=[start_date, end_date],
    product__is_available=True  # Solo contar productos disponibles
    ).aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0

    # Ventas por método de pago
    payment_methods = Sale.objects.filter(
        date__range=[start_date, end_date]
    ).values('payment_method').annotate(
        count=Count('id'),
        total=Sum('total')
    )
    
    daily_sales = Sale.objects.filter(
    date__range=[start_date, end_date]
    ).annotate(
        day=TruncDate('date')
    ).values('day').annotate(
        count=Count('id'),
        total=Sum('total')
    ).order_by('day')

    
    # Productos más vendidos (solo productos disponibles)
    top_products = SaleItem.objects.filter(
    sale__date__range=[start_date, end_date],
    product__is_available=True
    ).values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('price'))
    ).order_by('-total_quantity')[:10]

    # Productos por categoría (solo productos disponibles)
    categories_data = Category.objects.annotate(
        count=Count('product', filter=Q(product__is_available=True)),  # Filtrar productos disponibles
        value=Sum(F('product__stock') * F('product__price'), filter=Q(product__is_available=True))  # Solo productos disponibles
    ).values('name', 'count', 'value')

    # Movimientos de stock por mes
    stock_movements = StockMovement.objects.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        in_qty=Sum('quantity', filter=Q(movement_type='IN')),
        out_qty=Sum('quantity', filter=Q(movement_type='OUT'))
    ).order_by('month')

    # Productos con stock bajo (solo productos disponibles)
    low_stock_products = Product.objects.filter(
        stock__lte=F('minimum_stock'),
        is_available=True  # Solo productos disponibles
    ).order_by('stock')

    context = {
        # Estadísticas generales
        'total_products': total_products,
        'total_stock': total_stock,
        'total_value': total_value,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        
        # Datos para gráficos
        'categories_data': json.dumps(list(categories_data), cls=DjangoJSONEncoder),
        'stock_movements': json.dumps(list(stock_movements), cls=DjangoJSONEncoder),
        'payment_methods': json.dumps(list(payment_methods), cls=DjangoJSONEncoder),
        'daily_sales': json.dumps(list(daily_sales), cls=DjangoJSONEncoder),
        'top_products': json.dumps(list(top_products), cls=DjangoJSONEncoder),
        
        # Datos para tablas
        'low_stock_products': low_stock_products,
        # Fechas del reporte
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'inventory/reports.html', context)
def sales_history(request):
    # Obtener todas las ventas (puedes agregar filtros según necesites)
    sales = Sale.objects.all().order_by('-date')  # Ordenar por la fecha más reciente
    sales_with_items = []

    # Recorrer las ventas para agregar los detalles de los artículos comprados
    for sale in sales:
        items = sale.items.all()  # Obtener todos los productos de la venta
        sale_details = {
            'sale': sale,
            'items': items,
            'total': sale.total
        }
        sales_with_items.append(sale_details)

    return render(request, 'inventory/sales_history.html', {'sales': sales_with_items})


def invoice_detail(request, id):
    sale = Sale.objects.get(id=id)  # Obtener la venta con el id
    return render(request, 'inventory/invoice_detail.html', {'sale': sale})

@login_required
def pos_view(request):
    categories = Category.objects.all()
    return render(request, 'inventory/pos.html', {
        'categories': categories
    })


def get_products(request):
    search = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    # Filtrar solo los productos disponibles
    products = Product.objects.filter(is_available=True)

    if search:
        products = products.filter(name__icontains=search)

    if category:
        products = products.filter(category__name__icontains=category)

    data = []
    for product in products:
        # Obtener la imagen principal (si existe)
        main_image = product.images.filter(is_main=True).first()

        # Si no hay imagen principal, usar la imagen secundaria (si existe)
        main_image_url = main_image.image.url if main_image else (product.image.url if product.image else '/static/img/no-image.png')

        # Agregar la información del producto, incluyendo la URL de la imagen
        data.append({
            'id': product.id,
            'name': product.name,
            'code': product.code,
            'price': product.price,
            'stock': product.stock,
            'main_image': main_image_url,  # Imagen principal (si existe)
            'image': product.image.url if product.image else None,  # Fallback a la imagen del producto

        })

    # Retornar los datos como JSON
    return JsonResponse(data, safe=False)


def get_product_by_code(request):
    code = request.GET.get('code', '').strip()
    
    if not code:
        return JsonResponse({'error': 'Código no proporcionado'}, status=400)
    
    # Asegurar que el código tenga exactamente 13 dígitos (añadir ceros a la izquierda si es necesario)
    code = code.zfill(13)

    try:
        # Primero buscar por código de producto
        try:
            # Buscar por código de producto o código de barras y asegurarse de que esté disponible
            product = Product.objects.get(Q(code=code) | Q(barcode=code), is_available=True)
        except Product.DoesNotExist:
            # Si no se encuentra, buscar por código de barras
            product = Product.objects.get(barcode=code)
    # Obtener la imagen principal (ya sea la de 'image' del producto o la de 'ProductImage' con is_main=True)
        main_image = product.get_main_image()  # Método para obtener la imagen principal
        main_image_url = main_image.url if main_image else None

        # Obtener las otras imágenes de la galería
        gallery_images = []
        for product_image in product.get_gallery_images():
            gallery_images.append(product_image.image.url)
        
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'stock': product.stock,
            'image': product.image.url if product.image else None,
            'main_image': main_image_url,  # Imagen principal
            'gallery_images': gallery_images,  # Otras imágenes de la galería
            'barcode': product.barcode,
            'barcode_image': product.barcode_image.url if product.barcode_image else None,
            'qr_code': product.qr_code.url if product.qr_code else None
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'error': f'No se encontró ningún producto con el código: {code}'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'error': f'Error al buscar el producto: {str(e)}'
        }, status=500)
@transaction.atomic
def create_sale(request):
    try:
        data = json.loads(request.body)
        items = data.get('items', [])

        if not items:
            return JsonResponse({'error': 'No hay items en la venta'}, status=400)

        # Crear venta
        sale = Sale.objects.create(
            customer_name=data.get('customer_name', 'CONSUMIDOR FINAL'),
            customer_id=data.get('customer_id', '9999999999'),
            payment_method=data.get('payment_method', 'CASH'),
            notes=data.get('notes', ''),
            seller=request.user
        )

        # Crear los productos de la venta (SaleItem)
        for item in items:
            product_id = item.get('product_id')
            quantity = int(item.get('quantity', 0))
            price = Decimal(str(item.get('price', '0')))

            # Validación del stock antes de crear los SaleItems
            try:
                product = Product.objects.select_for_update().get(id=product_id)
            except Product.DoesNotExist:
                transaction.set_rollback(True)
                return JsonResponse({'error': f'Producto con ID {product_id} no encontrado'}, status=404)

            if product.stock < quantity:
                transaction.set_rollback(True)
                return JsonResponse(
                    {'error': f'Stock insuficiente para {product.name} (disponible: {product.stock})'},
                    status=400
                )

            # Crear el SaleItem sin modificar stock aún
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                price=price
            )

        # Después de crear todos los SaleItems, actualizamos el stock y registramos los movimientos
        for item in sale.items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()

            # Crear movimiento de stock
            StockMovement.objects.create(
                product=product,
                movement_type='OUT',
                quantity=item.quantity,
                notes=f'Venta #{sale.number}'
            )

        # Actualizar totales de la venta
        sale.update_totals()

        # Detalles de la venta
        sale_details = {
            'success': True,
            'sale_id': sale.id,
            'sale_number': sale.number,
            'customer_name': sale.customer_name,
            'customer_id': sale.customer_id,
            'date': sale.date.strftime('%Y-%m-%d %H:%M:%S'),
            'payment_method': dict(Sale.PAYMENT_METHODS)[sale.payment_method],
            'items': [{
                'name': item.product.name,
                'quantity': item.quantity,
                'price': str(item.price),
                'subtotal': str(item.subtotal)
            } for item in sale.items.all()],
            'subtotal': str(sale.subtotal),
            'tax': str(sale.tax),
            'total': str(sale.total)
        }

        return JsonResponse(sale_details)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al procesar los datos JSON'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Error al procesar la venta'}, status=400)

@login_required
def get_receipt(request, sale_number):
    try:
        sale = Sale.objects.select_related('seller').prefetch_related(
            'items__product'
        ).get(number=sale_number)
        
        # Obtener la primera empresa desde la base de datos
        company = Company.objects.first()  # O puedes usar otro filtro si hay más de una empresa

        context = {
            'sale': sale,
            'items': sale.items.all(),
            'company': company  # Pasar el objeto de la empresa al contexto
        }
        return render(request, 'inventory/receipt.html', context)
    except Sale.DoesNotExist:
        return JsonResponse({'error': 'Venta no encontrada'}, status=404)
@login_required
@user_passes_test(is_admin)
def company_detail(request):
    company = Company.objects.first()

    if not company:
        company = Company.objects.create(
            name="Default Company",
            ruc="0000000000",
            address="Default Address",
            phone="000-000-0000",
            email="default@example.com"
        )
    
    # Obtener TODAS las certificaciones
    all_certifications = Certification.objects.all()
    print(all_certifications)  # Esto imprimirá la lista de certificaciones en la terminal

    certification_form = CertificationForm()
    form = CompanyForm(instance=company)
    
    if request.method == 'POST':
        if 'save_company' in request.POST:
            form = CompanyForm(request.POST, request.FILES, instance=company)
            if form.is_valid():
                try:
                    company = form.save()
                    messages.success(request, "Información de la empresa actualizada correctamente.")
                    return redirect('admin_company_detail')
                except Exception as e:
                    print(f"Error saving form: {e}")
                    messages.error(request, f"Error al guardar: {e}")
            else:
                print("Form errors:", form.errors)
                messages.error(request, "Error al guardar la información. Por favor revise los campos.")
        
        elif 'add_certification' in request.POST:
            certification_form = CertificationForm(request.POST, request.FILES)
            if certification_form.is_valid():
                certification = certification_form.save()
                company.certifications.add(certification)
                messages.success(request, "Certificación agregada correctamente.")
                return redirect('admin_company_detail')
            else:
                messages.error(request, "Error al agregar la certificación.")
    
    return render(request, 'admin_dashboard/company/detail.html', {
        'form': form,
        'company': company,
        'certification_form': certification_form,
        'certifications': all_certifications  # Aquí es donde pasas todas las certificaciones
    })
    
    
def edit_certification(request, id):
    # Obtener la certificación con el id proporcionado
    certification = get_object_or_404(Certification, id=id)

    if request.method == 'POST':
        # Si el formulario es válido, guardar los cambios
        certification_form = CertificationForm(request.POST, request.FILES, instance=certification)
        if certification_form.is_valid():
            certification_form.save()  # Guardar la certificación actualizada
            messages.success(request, "La certificación se ha actualizado correctamente.")
            return redirect('company_detail')  # Redirigir al detalle de la empresa
    else:
        # Si la petición es GET, simplemente mostrar el formulario con los datos actuales
        certification_form = CertificationForm(instance=certification)

    return render(request, 'edit_certification.html', {'certification_form': certification_form})

def delete_certification(request, id):
    # Obtener la certificación con el id proporcionado
    certification = get_object_or_404(Certification, id=id)

    # Eliminar la certificación
    certification.delete()
    messages.success(request, "La certificación ha sido eliminada correctamente.")

    # Redirigir al detalle de la empresa después de la eliminación
    return redirect('company_detail')


@login_required
@require_http_methods(["POST"])
@transaction.atomic
def create_quote(request):
    try:
        # Verificar que el contenido es JSON
        if not request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'error': 'Content-Type must be application/json'}, status=400)
            
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
        items = data.get('items', [])
        
        if not items:
            return JsonResponse({'error': 'No items in quote'}, status=400)
        
        # Calcular totales
        subtotal = sum(float(item['price']) * item['quantity'] for item in items)
        tax = subtotal * 0.15  # 15% IVA
        total = subtotal + tax
        
        # Crear cotización
        quote = Quote.objects.create(
            customer_name=data.get('customer_name', ''),
            customer_id=data.get('customer_id', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            subtotal=subtotal,
            tax=tax,
            total=total,
            notes=data.get('notes', ''),
            validity_days=data.get('validity_days', 15),
            created_by=request.user
        )
        print(f"Generated quote_number: {quote.quote_number}")  # <-- Imprime el valor

        # Crear items de la cotización
        quote_items = []
        for item in items:
            product = Product.objects.get(id=item['product_id'])
            quote_item = QuoteItem.objects.create(
                quote=quote,
                product=product,
                quantity=item['quantity'],
                price=item['price'],
                subtotal=float(item['price']) * item['quantity']
            )
            quote_items.append({
                'name': product.name,
                'quantity': quote_item.quantity,
                'price': float(quote_item.price),
                'subtotal': float(quote_item.subtotal)
            })
        
        return JsonResponse({
    'success': True,
    'quote_number': quote.quote_number,
    'date': quote.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    'customer_name': quote.customer_name,
    'customer_id': quote.customer_id,
    'email': quote.email,
    'phone': quote.phone,
    'items': [{
        'name': product.name,
        'quantity': item['quantity'],
        'price': float(item['price']),
        'subtotal': float(item['price']) * item['quantity']
    } for item in items],
    'subtotal': float(quote.subtotal),
    'tax': float(quote.tax),
    'total': float(quote.total),
    'validity_days': quote.validity_days
})

        
    except Product.DoesNotExist:
        return JsonResponse({'error': 'One or more products not found'}, status=400)
    except Exception as e:
        # Log the error for debugging
        print(f"Error creating quote: {str(e)}")
        return JsonResponse({'error': 'Error creating quote'}, status=500)

@login_required
def quote_to_sale(request, quote_number):
    try:
        quote = Quote.objects.get(quote_number=quote_number)
        
        if quote.is_converted:
            return JsonResponse({'error': 'Quote already converted to sale'}, status=400)
        
        # Crear venta desde la cotización
        sale = Sale.objects.create(
            customer_name=quote.customer_name,
            customer_id=quote.customer_id,
            subtotal=quote.subtotal,
            tax=quote.tax,
            total=quote.total,
            notes=f"Converted from Quote #{quote.quote_number}\n{quote.notes}",
            created_by=request.user
        )
        
        # Crear items de la venta y actualizar stock
        for quote_item in quote.items.all():
            product = quote_item.product
            
            if product.stock < quote_item.quantity:
                sale.delete()
                return JsonResponse({
                    'error': f'Insufficient stock for {product.name}'
                }, status=400)
            
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quote_item.quantity,
                price=quote_item.price,
                subtotal=quote_item.subtotal
            )
            
            # Actualizar stock
            product.stock -= quote_item.quantity
            product.save()
        
        # Marcar cotización como convertida
        quote.is_converted = True
        quote.save()
        
        return JsonResponse({
            'success': True,
            'sale_number': sale.sale_number
        })
        
    except Quote.DoesNotExist:
        return JsonResponse({'error': 'Quote not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@login_required
def quote_pdf(request, quote_number):
    # Obtén la cotización a partir del número de cotización
    quote = get_object_or_404(Quote, quote_number=quote_number)
    company = Company.objects.first()  # O puedes usar otro filtro si hay más de una empresa

    # Renderiza el HTML que se usará para generar el PDF
    html = render_to_string('pos/quote_pdf.html', {'quote': quote, 'company': company})

    # Crea la respuesta Http con el contenido tipo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="quote_{quote_number}.pdf"'

    # Usa xhtml2pdf para convertir el HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Si la conversión falla, muestra un mensaje de error
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    # Devuelve la respuesta con el PDF
    return response




from django.shortcuts import render, get_object_or_404
from .models import Category
from django.shortcuts import render, get_object_or_404
from .models import Category

def base_product(request, category_id=None):
    # Obtener todas las categorías para la barra lateral
    all_categories = Category.objects.all()

    # Manejar el caso donde no se selecciona ninguna categoría
    current_category = None
    if category_id is not None and category_id != 0:  
        current_category = get_object_or_404(Category, id=category_id)

    # Obtener categoría seleccionada de los parámetros GET
    selected_category_id = request.GET.get('category')

    context = {
        "all_categories": all_categories,
        "current_category": current_category,
        "selected_category_id": selected_category_id,
    }

    return render(request, "products/base_productos.html", context)
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Category, Product, Brand


def apply_filters_and_sorting(products, request):
    """Función auxiliar para aplicar filtros y ordenamiento"""
    price_range = request.GET.get('price_range')
    sort_by = request.GET.get('sort_by', 'relevance')
    selected_category_id = request.GET.get('category')
    selected_brand_id = request.GET.get('brand')

    # Filtrar por categoría si se especifica y no es 'all'
    if selected_category_id and selected_category_id != 'all':
        try:
            category_id = int(selected_category_id)
            products = products.filter(category_id=category_id)
        except (ValueError, TypeError):
            # Si no se puede convertir a entero, intentar como string
            products = products.filter(category__slug=selected_category_id)
    
    # Filtrar por marca si se especifica y no es 'all'
    if selected_brand_id and selected_brand_id != 'all':
        try:
            brand_id = int(selected_brand_id)
            products = products.filter(brand_id=brand_id)
        except (ValueError, TypeError):
            products = products.filter(brand__slug=selected_brand_id)
        
    # Filtrar por precio máximo
    if price_range:
        try:
            price_range = float(price_range)
            products = products.filter(price__lte=price_range)
        except (ValueError, TypeError):
            pass

    # Aplicar ordenamiento
    ordering_options = {
        'price-asc': 'price',
        'price-desc': '-price',
        'name-asc': 'name',
        'name-desc': '-name',
        'newest': '-created_at',  # Añadido para ordenar por más recientes
    }
    if sort_by in ordering_options:
        products = products.order_by(ordering_options[sort_by])
    else:
        # Ordenamiento por relevancia (productos con descuento primero)
        products = products.order_by('-discount', '-id')

    return products, selected_category_id, selected_brand_id, sort_by, price_range

def cliente_home(request, product_id=None):
    # Si se pasa un product_id, redirige a la página de detalles del producto
    if product_id:
        product = get_object_or_404(Product, id=product_id, is_available=True)
        category = product.category
        return redirect('category_detail', category_id=category.id, product_id=product.id)
    
    # Obtener todas las categorías y marcas
    all_categories = Category.objects.all()
    all_brands = Brand.objects.all()

    # Si no hay categorías, renderizar sin productos
    if not all_categories.exists():
        return render(request, 'products/category_detail.html', {
            'category': None,
            'products': [],
            'all_categories': [],
            'all_brands': all_brands,
            'selected_category': None,
            'is_cliente_home': True
        })
    
    # Obtener todos los productos disponibles
    products = Product.objects.filter(is_available=True)
    
    # Aplicar búsqueda por nombre si existe
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Calcular el precio máximo para el slider
    max_price_product = products.order_by('-price').first()
    max_price = max_price_product.price if max_price_product else 1000
    max_price = (int(max_price / 100) + 1) * 100  # Redondear hacia arriba al siguiente 100
    
    # Aplicar filtros y ordenamiento
    products, selected_category_id, selected_brand_id, sort_by, price_range = apply_filters_and_sorting(products, request)
    
    # Si no se especificó un precio máximo, usar el máximo calculado
    if not price_range:
        price_range = max_price
    else:
        price_range = float(price_range)
        
    # Seleccionar la categoría activa
    selected_category_obj = None
    if selected_category_id and selected_category_id != 'all':
        try:
            selected_category_obj = Category.objects.get(id=selected_category_id)
        except Category.DoesNotExist:
            selected_category_obj = None
    
    # Si es una solicitud AJAX, devolver JSON con productos
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        products_data = [{
            'id': product.id,
            'name': product.name,
            'code': product.code,
            'description': product.description,
            'price': float(product.price),
            'image': product.get_main_image().url if product.get_main_image() else None,
            'stock': product.stock,
            'category_id': product.category.id,
            'category_name': product.category.name,
            'is_available': product.is_available,
            'discount': float(product.discount),
        } for product in products]
        return JsonResponse({'products': products_data})
    
    # Pasar todas las categorías al template
    context = {
        'category': selected_category_obj or (all_categories.first() if all_categories.exists() else None),
        'products': products,
        'all_categories': all_categories,
        'all_brands': all_brands,
        'selected_category': selected_category_id if selected_category_id else 'all',
        'selected_category_obj': selected_category_obj,
        'selected_brand': selected_brand_id if selected_brand_id else 'all',
        'sort_by': sort_by,
        'price_range': price_range,
        'max_price': max_price,
        'search_query': search_query,
        'is_cliente_home': True
    }
    
    return render(request, 'products/category_detail.html', context)


def category_detail(request, category_id, product_id=None):
    category = get_object_or_404(Category, id=category_id)
    
    # Si se solicita un producto específico
    if product_id:
        product = get_object_or_404(Product, id=product_id, is_available=True)

        if product.category.id != category_id:
            return redirect('category_detail', category_id=product.category.id, product_id=product.id)
            
        # Obtener las imágenes de la galería
        gallery_images = product.get_gallery_images()
        main_image = product.get_main_image()
        # Dividir las características en una lista
        features = product.features.split(',') if product.features else []

        return render(request, 'products/product_detail.html', {
            'product': product,
            'category': product.category,
            'features': features,
            'gallery_images': gallery_images,
            'main_image': main_image
        })

    # Inicialmente, filtrar productos por la categoría de la página
    products = Product.objects.filter(is_available=True, category=category)
    
    # Obtener parámetros de filtro
    selected_category_id = request.GET.get('category', str(category.id))
    selected_brand_id = request.GET.get('brand')
    
    # Si se selecciona una categoría diferente, actualizar los productos
    if selected_category_id and selected_category_id != 'all' and selected_category_id != str(category.id):
        try:
            selected_category = Category.objects.get(id=selected_category_id)
            products = Product.objects.filter(is_available=True, category=selected_category)
        except Category.DoesNotExist:
            # Mantener la categoría actual si no existe la seleccionada
            selected_category_id = str(category.id)
    
    # Aplicar búsqueda por nombre si existe
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Calcular el precio máximo para el slider
    all_products = Product.objects.filter(is_available=True)
    max_price_product = all_products.order_by('-price').first()
    max_price = max_price_product.price if max_price_product else 1000
    max_price = (int(max_price / 100) + 1) * 100  # Redondear hacia arriba al siguiente 100
    
    # Aplicar filtros y ordenamiento
    products, selected_category_id, selected_brand_id, sort_by, price_range = apply_filters_and_sorting(products, request)

    # Si no se especificó un precio máximo, usar el máximo calculado
    if not price_range:
        price_range = max_price
    else:
        price_range = float(price_range)

    # Obtener el objeto de categoría seleccionada
    selected_category_obj = None
    if selected_category_id and selected_category_id != 'all':
        try:
            selected_category_obj = Category.objects.get(id=selected_category_id)
        except Category.DoesNotExist:
            selected_category_obj = category  # Usar la categoría actual si no existe la seleccionada
    else:
        selected_category_obj = category  # Usar la categoría actual si no hay selección
    
    # Si es una solicitud AJAX, devolver JSON con productos
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        products_data = [{
            'id': product.id,
            'name': product.name,
            'code': product.code,
            'description': product.description,
            'price': float(product.price),
            'image': product.get_main_image().url if product.get_main_image() else None,
            'gallery_images': [img.image.url for img in product.get_gallery_images()],
            'stock': product.stock,
            'category_id': product.category.id,
            'category_name': product.category.name,
            'is_available': product.is_available,
            'discount': float(product.discount),
        } for product in products]
        return JsonResponse({'products': products_data})
    
    # Obtener todas las marcas para el filtro en el template
    all_brands = Brand.objects.all()
    
    context = {
        'category': category,
        'selected_category': selected_category_id,        
        'selected_category_obj': selected_category_obj,
        'selected_brand': selected_brand_id if selected_brand_id else 'all',
        'products': products,
        'all_categories': Category.objects.all(),
        'all_brands': all_brands,
        'sort_by': sort_by,
        'price_range': price_range,
        'max_price': max_price,
        'search_query': search_query,
        'is_category_detail': True
    }

    return render(request, 'products/category_detail.html', context)

    



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    # Verificar si el producto está sin stock
    if product.stock == 0:
        messages.error(request, f"No se puede agregar {product.name} al carrito. NO HAY STOCK DISPONIBLE.")
        return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
    
    # Verificar si el stock actual es mayor que el stock mínimo
    if product.stock <= product.minimum_stock:
        messages.error(request, f"No se puede agregar {product.name} al carrito. Stock insuficiente (nivel mínimo alcanzado).")
        return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
    
    # Obtener las imágenes de la galería y la imagen principal
    gallery_images = [img.image.url for img in product.get_gallery_images()]
    main_image = product.get_main_image().url if product.get_main_image() else None
    
    product_id_str = str(product_id)
    
    # Verificar si agregar más unidades excedería el stock disponible
    current_quantity = cart.get(product_id_str, {}).get('quantity', 0)
    if product_id_str in cart and current_quantity + 1 > product.stock:
        messages.warning(request, f"No hay suficiente stock de {product.name} para agregar más unidades.")
        return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            "name": product.name,
            "price": float(product.price),
            "quantity": 1,
            "subtotal": float(product.price),
            "main_image": main_image,
            "gallery_images": gallery_images
        }
    
    # Actualizar subtotales
    cart[product_id_str]['subtotal'] = cart[product_id_str]['price'] * cart[product_id_str]['quantity']
    
    request.session['cart'] = cart
    messages.success(request, f"{product.name} agregado al carrito.")
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))



def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        if cart[product_id_str]['quantity'] > 1:
            cart[product_id_str]['quantity'] -= 1
            cart[product_id_str]['subtotal'] = cart[product_id_str]['price'] * cart[product_id_str]['quantity']
            messages.success(request, "Cantidad actualizada.")
        else:
            del cart[product_id_str]
            messages.success(request, "Producto eliminado del carrito.")
    
    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    
    # Asegurarse de que cada elemento del carrito tenga la clave 'subtotal'
    for product_id, item in cart.items():
        if 'subtotal' not in item:
            item['subtotal'] = item['price'] * item['quantity']
    
    # Actualizar el carrito en la sesión
    request.session['cart'] = cart
    
    # Ahora podemos calcular el total de forma segura
    total_price = sum(item['subtotal'] for item in cart.values())
    
    # Calcular el IVA
    iva_amount = total_price * 0.15
    total_with_iva = total_price + iva_amount

    # Obtener una categoría para el botón "Seguir comprando"
    category = Category.objects.first()

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'total_price': total_price,
        'iva_amount': iva_amount,
        'total_with_iva': total_with_iva,
        'category': category
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        messages.success(request, "Producto eliminado del carrito.")

    return redirect('cart_detail')


def clear_cart(request):
    request.session['cart'] = {}
    messages.success(request, "Carrito vaciado.")
    return redirect('cart_detail')


def cart_data(request):
    cart = request.session.get('cart', {})
    cart_items = list(cart.values())
    total_items = sum(item['quantity'] for item in cart.values())

    return JsonResponse({'cart_items': cart_items, 'total_items': total_items})


def checkout(request):
    # Verificar si el usuario está autenticado
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para realizar la compra.")
        return redirect('login')  # Redirigir a la página de login si no está autenticado

    # Verificar si hay productos en el carrito
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "No hay productos en el carrito para realizar la compra.")
        return redirect('cart_detail')
        
    return render(request, 'cart/checkout.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Count
from decimal import Decimal
import json
import uuid

from .models import Order, OrderItem, Product

from decimal import Decimal
from decimal import Decimal
import random
import string

# Función para generar el número de pedido
def generate_order_number():
    """Genera un número de orden único y aleatorio."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def process_order(request):
    # Verificar si el usuario está autenticado
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': "Debes iniciar sesión para procesar el pedido."})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Obtener los productos del carrito
            cart = request.session.get('cart', {})
            if not cart:
                return JsonResponse({'success': False, 'message': "No hay productos en el carrito para realizar la compra."})

            # Verificar si es recoger en tienda
            shipping_method = data.get('shipping_method', 'pickup')  # Default to pickup
            
            # Calcular el total del pedido asegurando que subtotal sea Decimal
            subtotal = sum(Decimal(str(item['subtotal'])) for item in cart.values())  # Convertimos a Decimal
            tax = subtotal * Decimal('0.15')  # 15% IVA
            
            # Si es recoger en tienda, el costo de envío es 0
            if shipping_method == 'pickup':
                shipping_cost = Decimal('0.00')
            else:
                shipping_cost = Decimal(str(data.get('shipping_cost', '5.00')))  # Convertir shipping_cost a Decimal
                
            total = subtotal + tax + shipping_cost  # Suma sin errores

            # Crear un nuevo pedido en la base de datos con datos de entrega
            order = Order.objects.create(
                user=request.user,
                order_number=data.get('order_number', generate_order_number()),  # Usar la función aquí
                total=total,
                status='pending',
                date=timezone.now(),
                email=data.get('email'),
                phone=data.get('phone'),
                fullname=data.get('fullname'),
                address=data.get('address', '') if shipping_method != 'pickup' else '',  # Opcional si es recoger en tienda
                city=data.get('city', '') if shipping_method != 'pickup' else '',  # Opcional si es recoger en tienda
                postal_code=data.get('postal', '') if shipping_method != 'pickup' else '',  # Opcional si es recoger en tienda
                state=data.get('state', '') if shipping_method != 'pickup' else '',  # Opcional si es recoger en tienda
                payment_method=data.get('payment_method'),
                shipping_method=shipping_method,  # Guardar el método de envío
                shipping_cost=shipping_cost
            )
            
            # Guardar los productos del carrito en el modelo OrderItem
            for item in cart.values():
                product = Product.objects.get(name=item['name'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=Decimal(str(item['price'])),  # Convertir precio a Decimal
                )
            
            # Vaciar el carrito después de realizar el pedido
            request.session['cart'] = {}
            request.session.modified = True  # Asegurarse de que los cambios se guarden

            return JsonResponse({
                'success': True, 
                'message': 'Pedido procesado correctamente', 
                'order_id': order.id,
                'order_number': order.order_number
            })

        except Product.DoesNotExist as e:
            return JsonResponse({'success': False, 'message': f'Producto no encontrado: {str(e)}'})
        except Exception as e:
            import traceback
            print(traceback.format_exc())  # Imprimir el error completo en la consola del servidor
            return JsonResponse({'success': False, 'message': f'Error al procesar el pedido: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Método no permitido'})


def order_success(request, order_id=None):
    # Mostrar el pedido exitoso
    if not order_id:
        messages.error(request, "No se pudo procesar el pedido.")
        return redirect('cart_detail')

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "El pedido no existe.")
        return redirect('cart_detail')

    return render(request, 'cart/order_success.html', {'order': order})


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.db.models.functions import Cast
from django.db.models.fields import DateTimeField
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
from .models import Order

def view_orders(request):
    # Obtener parámetros de filtrado y búsqueda
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    tab_filter = request.GET.get('tab', 'all')
    sort_param = request.GET.get('sort', '-date')  # Por defecto, ordenar por fecha descendente
    
    # Iniciar la consulta base
    if request.user.is_staff:
        orders_query = Order.objects.all().select_related('user')
    else:
        orders_query = Order.objects.filter(user=request.user).select_related('user')
    
    # Aplicar filtro de pestaña
    if tab_filter != 'all':
        orders_query = orders_query.filter(status=tab_filter)
    
    # Aplicar filtro de estado
    if status_filter != 'all':
        orders_query = orders_query.filter(status=status_filter)
    
    # Aplicar búsqueda
    if search_query:
        orders_query = orders_query.filter(
            Q(id__icontains=search_query) | 
            Q(fullname__icontains=search_query) | 
            Q(email__icontains=search_query) | 
            Q(address__icontains=search_query)
        )
    
    # Aplicar ordenamiento
    if sort_param.startswith('-'):
        orders_query = orders_query.order_by(sort_param)
    else:
        orders_query = orders_query.order_by(sort_param)
    
    # Desactivar temporalmente la conversión de zona horaria para esta consulta
    # Esto evita el error de utcoffset
    with timezone.override(None):
        # Paginación
        paginator = Paginator(orders_query, 10)  # 10 pedidos por página
        page_number = request.GET.get('page', 1)
        orders_page = paginator.get_page(page_number)
    
    # Contar pedidos por estado para las estadísticas
    pending_count = Order.objects.filter(status='pending').count()
    processing_count = Order.objects.filter(Q(status='processing') | Q(status='shipped')).count()
    completed_count = Order.objects.filter(status='completed').count()
    
    context = {
        'orders': orders_page,
        'pending_count': pending_count,
        'processing_count': processing_count,
        'completed_count': completed_count,
    }
    
    return render(request, 'orders/order_list.html', context)
def order_detail(request, order_id):
    # Obtiene el pedido y sus productos
    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all().select_related('product')
    
    # Calcular el total del pedido
    total_price = sum(Decimal(item.price) * Decimal(item.quantity) for item in order_items)
    
    # Calcular el IVA (15%)
    iva_amount = total_price * Decimal('0.15')
    total_with_iva = total_price + iva_amount + order.shipping_cost
    
    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
        'iva_amount': iva_amount,
        'total_with_iva': total_with_iva
    }
    
    return render(request, 'orders/order_detail.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Order
from django.contrib import messages
from django.utils import timezone

def update_order_status(request, order_id):
    # Asegúrate de que solo los administradores puedan actualizar el estado
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST":
        # Obtén el nuevo estado del formulario
        new_status = request.POST.get('status')
        
        # Validar que el estado sea válido y no exceda la longitud máxima
        valid_statuses = [status[0] for status in Order.STATUS_CHOICES]
        if new_status and new_status in valid_statuses:
            # Guardar el estado anterior para comparar
            old_status = order.status
            
            # Actualizar el estado
            order.status = new_status
            
            # Registrar la fecha del cambio de estado
            now = timezone.now()
            if new_status == 'processing' and old_status == 'pending':
                order.processing_date = now
            elif new_status == 'shipped' and old_status == 'processing':
                order.shipping_date = now
                
                # Si hay un número de seguimiento en el formulario, guardarlo
                tracking_number = request.POST.get('tracking_number')
                if tracking_number:
                    order.tracking_number = tracking_number
                    
            elif new_status == 'completed' and old_status == 'shipped':
                order.completion_date = now
            elif new_status == 'canceled':
                order.cancellation_date = now
                
                # Guardar el motivo de cancelación si existe
                cancel_reason = request.POST.get('cancel_reason')
                if cancel_reason:
                    order.cancel_reason = cancel_reason
            
            try:
                order.save()
                messages.success(request, f"El estado del pedido #{order_id} ha sido actualizado a {dict(Order.STATUS_CHOICES)[new_status]}.")
            except Exception as e:
                messages.error(request, f"Error al actualizar el estado: {str(e)}")
        else:
            messages.error(request, "El estado proporcionado no es válido.")
            
        # Redirigir a la página de detalles si venimos de ahí
        referer = request.META.get('HTTP_REFERER', '')
        if f'/orders/{order_id}/' in referer or f'/order/{order_id}/' in referer:
            return redirect('order_detail', order_id=order_id)
        
        return redirect('view_orders')
    
    # Redirige si no es un POST
    return redirect('view_orders')




def delete_order(request, order_id):
    # Verificar que el usuario sea un administrador
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    
    # Obtener el pedido a eliminar
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST":
        # Eliminar el pedido
        order.delete()
        messages.success(request, f"El pedido #{order_id} ha sido eliminado correctamente.")
        return redirect('view_orders')
    
    # Si no es POST, redirige sin cambios
    return redirect('view_orders')


def add_tracking(request, order_id):
    """Añadir número de seguimiento a un pedido enviado"""
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST" and order.status == 'shipped':
        tracking_number = request.POST.get('tracking_number')
        if tracking_number:
            order.tracking_number = tracking_number
            order.save()
            messages.success(request, "Número de seguimiento añadido correctamente.")
        
        return redirect('order_detail', order_id=order_id)
    
    return redirect('order_detail', order_id=order_id)


def print_invoice(request, order_id):
    """Vista para imprimir la factura"""
    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all().select_related('product')
    
    # Calcular el total del pedido
    total_price = sum(Decimal(item.price) * Decimal(item.quantity) for item in order_items)
    iva_amount = total_price * Decimal('0.15')
    total_with_iva = total_price + iva_amount + order.shipping_cost
    
    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
        'iva_amount': iva_amount,
        'total_with_iva': total_with_iva,
        'print_mode': True  # Para indicar que es modo impresión
    }
    
    return render(request, 'orders/print_invoice.html', context)

def base_product(request, category_id):
    category = get_object_or_404(category, id=category_id)
    return render(request, "products/base_productos.html", {"category": category})


def prueba(request):
    return render(request, "dashboard/cliente_base.html")






@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Estadísticas generales
    total_users = CustomUser.objects.count()
    total_products = Product.objects.filter(is_available=True).count()
    
    # Estadísticas de ventas (último mes)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    sales = Sale.objects.filter(date__range=[start_date, end_date])
    total_sales = sales.count()
    total_revenue = sales.aggregate(total=Sum('total'))['total'] or 0
    
    # Órdenes completadas y ganancias
    completed_orders = Order.objects.filter(status='completed')
    total_completed_orders = completed_orders.count()
    total_earnings = completed_orders.aggregate(total=Sum('total'))['total'] or 0
    
    # Órdenes completadas este mes
    monthly_completed_orders = completed_orders.filter(completion_date__range=[start_date, end_date])
    monthly_earnings = monthly_completed_orders.aggregate(total=Sum('total'))['total'] or 0
    
    # Productos con stock bajo
    low_stock_products = Product.objects.filter(
        is_available=True, 
        stock__lte=F('minimum_stock')
    )[:5]
    
    # Ventas recientes
    recent_sales = Sale.objects.order_by('-date')[:5]
    
    # Órdenes recientes completadas
    recent_completed_orders = Order.objects.filter(status='completed').order_by('-completion_date')[:5]
    
    # Datos para gráficos
    monthly_sales = Sale.objects.filter(
        date__year=timezone.now().year
    ).values('date__month').annotate(
        total=Sum('total')
    ).order_by('date__month')
    
    # Ventas por categoría
    category_sales = Category.objects.annotate(
        sales_count=Count('product__saleitem', distinct=True),
        sales_total=Sum('product__saleitem__subtotal')
    )
    
    # Ganancias mensuales de órdenes completadas
    monthly_order_earnings = Order.objects.filter(
        status='completed',
        completion_date__year=timezone.now().year
    ).values('completion_date__month').annotate(
        total=Sum('total')
    ).order_by('completion_date__month')
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'total_completed_orders': total_completed_orders,
        'total_earnings': total_earnings,
        'monthly_earnings': monthly_earnings,
        'low_stock_products': low_stock_products,
        'recent_sales': recent_sales,
        'recent_completed_orders': recent_completed_orders,
        'monthly_sales': list(monthly_sales),
        'monthly_order_earnings': list(monthly_order_earnings),
        'category_sales': category_sales,
    }
    
    return render(request, 'admin_dashboard/dashboard.html', context)


# Gestión de Usuarios
@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'admin_dashboard/users/list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'admin_dashboard/users/detail.html', {'user': user})

@login_required
@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_blocked = not user.is_blocked
    user.save()
    status = "bloqueado" if user.is_blocked else "desbloqueado"
    messages.success(request, f"Usuario {user.username} {status} correctamente.")
    return redirect('admin_user_list')

# Gestión de Productos
@login_required
@user_passes_test(is_admin)
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard/products/list.html', {'products': products})

# The issue is likely in your product_form view function

@login_required
@user_passes_test(is_admin)
def product_form(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        title = "Editar Producto"
    else:
        product = None
        title = "Nuevo Producto"
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar el producto primero - los códigos se generarán automáticamente
                    product = form.save()
                    
                    # Guardar el formset de imágenes
                    instances = formset.save(commit=False)
                    
                    # Procesar las imágenes eliminadas
                    for obj in formset.deleted_objects:
                        obj.delete()
                    
                    # Guardar las nuevas imágenes y actualizar las existentes
                    for instance in instances:
                        instance.product = product
                        instance.save()
                    
                    # Asegurarse de que haya una imagen principal
                    if not product.images.filter(is_main=True).exists() and product.images.exists():
                        first_image = product.images.first()
                        first_image.is_main = True
                        first_image.save()
                    
                    messages.success(request, f"Producto {'actualizado' if product_id else 'creado'} correctamente.")
                    return redirect('admin_product_list')
                    
            except Exception as e:
                messages.error(request, f"Error al {'actualizar' if product_id else 'crear'} el producto: {str(e)}")
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)
    
    context = {
        'form': form,
        'formset': formset,
        'title': title,
        'product': product,
        'is_edit': product_id is not None
    }
    
    return render(request, 'admin_dashboard/products/form.html', context)

# Vista auxiliar para manejar operaciones AJAX con las imágenes
@login_required
@user_passes_test(is_admin)
def handle_product_image(request, image_id=None):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        action = request.POST.get('action')
        
        try:
            if image_id:
                image = get_object_or_404(ProductImage, id=image_id)
                
                if action == 'delete':
                    was_main = image.is_main
                    product = image.product
                    image.delete()
                    
                    # Si era la imagen principal, establecer otra como principal
                    if was_main and product.images.exists():
                        new_main = product.images.first()
                        new_main.is_main = True
                        new_main.save()
                    
                    return JsonResponse({'status': 'success', 'message': 'Imagen eliminada correctamente'})
                    
                elif action == 'set_main':
                    product = image.product
                    # Quitar la marca de principal de todas las imágenes
                    product.images.update(is_main=False)
                    # Establecer esta imagen como principal
                    image.is_main = True
                    image.save()
                    return JsonResponse({'status': 'success', 'message': 'Imagen principal actualizada'})
                    
                elif action == 'reorder':
                    new_order = request.POST.get('order')
                    if new_order is not None:
                        image.order = int(new_order)
                        image.save()
                        return JsonResponse({'status': 'success', 'message': 'Orden actualizado'})
            
            return JsonResponse({'status': 'error', 'message': 'Acción no válida'}, status=400)
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
@login_required
@user_passes_test(is_admin)
def product_form(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        title = "Editar Producto"
    else:
        product = None
        title = "Nuevo Producto"
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar el producto primero
                    product = form.save()
                    
                    # Guardar el formset de imágenes
                    instances = formset.save(commit=False)
                    
                    # Procesar las imágenes eliminadas
                    for obj in formset.deleted_objects:
                        obj.delete()
                    
                    # Guardar las nuevas imágenes y actualizar las existentes
                    for instance in instances:
                        instance.product = product
                        instance.save()
                    
                    # Asegurarse de que haya una imagen principal
                    if not product.images.filter(is_main=True).exists() and product.images.exists():
                        first_image = product.images.first()
                        first_image.is_main = True
                        first_image.save()
                    
                    messages.success(request, f"Producto {'actualizado' if product_id else 'creado'} correctamente.")
                    return redirect('admin_product_list')
                    
            except Exception as e:
                messages.error(request, f"Error al {'actualizar' if product_id else 'crear'} el producto: {str(e)}")
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)
    
    context = {
        'form': form,
        'formset': formset,
        'title': title,
        'product': product,
        'is_edit': product_id is not None
    }
    
    return render(request, 'admin_dashboard/products/form.html', context)

# Vista auxiliar para manejar operaciones AJAX con las imágenes
@login_required
@user_passes_test(is_admin)
def handle_product_image(request, image_id=None):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        action = request.POST.get('action')
        
        try:
            if image_id:
                image = get_object_or_404(ProductImage, id=image_id)
                
                if action == 'delete':
                    was_main = image.is_main
                    product = image.product
                    image.delete()
                    
                    # Si era la imagen principal, establecer otra como principal
                    if was_main and product.images.exists():
                        new_main = product.images.first()
                        new_main.is_main = True
                        new_main.save()
                    
                    return JsonResponse({'status': 'success', 'message': 'Imagen eliminada correctamente'})
                    
                elif action == 'set_main':
                    product = image.product
                    # Quitar la marca de principal de todas las imágenes
                    product.images.update(is_main=False)
                    # Establecer esta imagen como principal
                    image.is_main = True
                    image.save()
                    return JsonResponse({'status': 'success', 'message': 'Imagen principal actualizada'})
                    
                elif action == 'reorder':
                    new_order = request.POST.get('order')
                    if new_order is not None:
                        image.order = int(new_order)
                        image.save()
                        return JsonResponse({'status': 'success', 'message': 'Orden actualizado'})
            
            return JsonResponse({'status': 'error', 'message': 'Acción no válida'}, status=400)
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)





@login_required
@user_passes_test(is_admin)
def toggle_product_availability(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_available = not product.is_available
    product.save()
    status = "disponible" if product.is_available else "no disponible"
    messages.success(request, f"Producto {product.name} marcado como {status}.")
    return redirect('admin_product_list')

# Gestión de Categorías
@login_required
@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.filter(parent__isnull=True).annotate(
        product_count=Count('product', filter=Q(product__is_available=True), distinct=True),
        total_stock=Sum('product__stock', filter=Q(product__is_available=True), distinct=True),
        total_value=Sum(F('product__stock') * F('product__price'), filter=Q(product__is_available=True), distinct=True),
        subcategory_count=Count('subcategories', distinct=True)  # Cuenta subcategorías
    )
    return render(request, 'admin_dashboard/categories/list.html', {'categories': categories})


@login_required
@user_passes_test(is_admin)
def category_form(request, category_id=None):
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        title = "Editar Categoría"
    else:
        category = None
        title = "Nueva Categoría"
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            return delete_category(request, category_id)

        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Categoría {'actualizada' if category else 'creada'} correctamente.")
            return redirect('admin_category_list')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'title': title,
        'category': category,
        'can_delete': category and category.product_count == 0 and category.subcategories.count() == 0  # Evita eliminar si tiene subcategorías
    }
    return render(request, 'admin_dashboard/categories/form.html', context)


@login_required
@user_passes_test(is_admin)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    # Verificar si la categoría tiene productos o subcategorías antes de eliminar
    if category.product_count > 0:
        messages.error(request, "No puedes eliminar una categoría que tiene productos asociados.")
        return redirect('admin_category_form', category_id=category.id)

    if category.subcategories.exists():
        messages.error(request, "No puedes eliminar una categoría que tiene subcategorías asociadas.")
        return redirect('admin_category_form', category_id=category.id)

    category.delete()
    messages.success(request, "Categoría eliminada correctamente.")
    return redirect('admin_category_list')
@login_required
@user_passes_test(is_admin)
def company_detail(request):
    company = Company.objects.first()  # Get the first company or create one if it doesn't exist
    if not company:
        company = Company.objects.create(
            name="Default Company",
            ruc="0000000000",
            address="Default Address",
            phone="000-000-0000",
            email="default@example.com"
        )
    
  
    # Certificaciones asociadas a la empresa
    certifications = company.certifications.all()

    # Certificaciones no asociadas
    all_certifications = Certification.objects.exclude(companies=company)
    certification_form = CertificationForm()
# Verificar que employee.id esté presente
    employees = company.employees.all()  # Asegúrate de que 'employees' tenga el id

    # Instanciar el formulario CompanyForm, siempre, fuera del POST
    form = CompanyForm(instance=company)
    
    if request.method == 'POST':
        if 'save_company' in request.POST:
            form = CompanyForm(request.POST, request.FILES, instance=company)
            
            # Debug information
            #print("POST data:", request.POST)
            #print("FILES data:", request.FILES)
            
            if form.is_valid():
                try:
                    company = form.save()
                    
                    # Handle certifications separately if needed
                    if 'certifications' in form.cleaned_data:
                        company.certifications.set(form.cleaned_data['certifications'])
                    
                    messages.success(request, "Información de la empresa actualizada correctamente.")
                    return redirect('admin_company_detail')
                except Exception as e:
                    print(f"Error saving form: {e}")
                    messages.error(request, f"Error al guardar: {e}")
            else:
                print("Form errors:", form.errors)
                for field, errors in form.errors.items():
                    print(f"Field {field} errors: {errors}")
                messages.error(request, "Error al guardar la información. Por favor revise los campos.")
        
        elif 'add_certification' in request.POST:
            certification_form = CertificationForm(request.POST, request.FILES)
            if certification_form.is_valid():
                certification = certification_form.save()
                # Add this certification to the company
                company.certifications.add(certification)
                messages.success(request, "Certificación agregada correctamente.")
                return redirect('admin_company_detail')
            else:
                messages.error(request, "Error al agregar la certificación.")
    
    return render(request, 'admin_dashboard/company/detail.html', {
        'form': form,
        'company': company,
        'certification_form': certification_form,
        'employees': employees,
        'certifications': certifications,  # Add certifications to the context
        'all_certifications': all_certifications,  # Pasa las certificaciones no asociadas

        
    })
@login_required
@user_passes_test(is_admin)
def delete_certification(request, certification_id):
    certification = get_object_or_404(Certification, id=certification_id)
    certification.delete()
    messages.success(request, "Certificación eliminada correctamente.")
    return redirect('admin_company_detail')
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmployeeForm
from .models import Employee, Company

@login_required
@user_passes_test(is_admin)
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            company = Company.objects.first()  # Asegúrate de que la empresa existe
            company.employees.add(employee)  # Agregar el empleado a la empresa
            messages.success(request, "Empleado agregado correctamente.")
            return redirect('admin_company_detail')
        else:
            messages.error(request, "Hubo un error al agregar el empleado.")
    else:
        form = EmployeeForm()

    return render(request, 'admin_dashboard/company/detail.html', {'form': form})
@login_required
@user_passes_test(is_admin)
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            # Si no se proporciona una nueva imagen, mantener la actual
            if 'profile_picture' in request.FILES:
                employee = form.save()
            else:
                employee = form.save(commit=False)
                # Asegurarse de no sobrescribir la imagen existente con None
                if hasattr(employee, 'profile_picture') and employee.profile_picture:
                    form.cleaned_data['profile_picture'] = employee.profile_picture
                employee.save()
                
            messages.success(request, "Empleado actualizado correctamente.")
            return redirect('admin_company_detail')
        else:
            messages.error(request, "Hubo un error al actualizar el empleado.")
    
    return redirect('admin_company_detail')

@login_required
@user_passes_test(is_admin)
def delete_employee(request, employee_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=employee_id)
        company = Company.objects.first()
        
        # Eliminar la relación con la empresa
        company.employees.remove(employee)
        
        # Opcionalmente, eliminar el empleado completamente de la base de datos
        employee.delete()
        
        messages.success(request, "Empleado eliminado correctamente.")
    
    return redirect('admin_company_detail')

# Reportes y Estadísticas Combinados
from django.utils import timezone
from django.db.models import Sum, Count, F
from django.contrib import messages
from .models import Sale, SaleItem, Order, OrderItem
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.http import HttpResponse
from io import BytesIO
import xlsxwriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

@login_required
@user_passes_test(is_admin)
def sales_report(request):
    # Obtener el rango de fechas (último mes por defecto)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    if request.GET.get('start_date') and request.GET.get('end_date'):
        try:
            start_date = timezone.make_aware(datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d'))
            end_date = timezone.make_aware(datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d'))
            end_date = end_date.replace(hour=23, minute=59, second=59)  # Ajustar al final del día
        except ValueError:
            messages.error(request, "Formato de fecha inválido. Use YYYY-MM-DD.")
            return redirect('admin_sales_report')

    # Obtener todas las ventas para verificar
    all_sales = Sale.objects.all()
    total_sales_count = all_sales.count()

    # Estadísticas de ventas
    sales = Sale.objects.filter(date__range=[start_date, end_date]).order_by('-date')
    filtered_sales_count = sales.count()
    sales_revenue = sales.aggregate(total=Sum('total'))['total'] or 0
    
    # Estadísticas de órdenes
    all_orders = Order.objects.all()
    total_orders_count = all_orders.count()

    orders = Order.objects.filter(date__range=[start_date, end_date]).order_by('-date')
    filtered_orders_count = orders.count()

    # Filtrar órdenes completadas para el cálculo de ingresos
    completed_orders = orders.filter(status='completed')
    orders_revenue = completed_orders.aggregate(total=Sum('total'))['total'] or 0

    # Total combinado (solo incluye órdenes completadas en el ingreso)
    total_transactions = filtered_sales_count + filtered_orders_count
    total_revenue = sales_revenue + orders_revenue
    
    # Ventas por método de pago
    payment_methods_sales = (
        sales.values('payment_method')
        .annotate(
            count=Count('id'),
            total=Sum('total')
        )
        .order_by('-total')
    )
    
    # Órdenes por método de pago
    payment_methods_orders = (
        orders.values('payment_method')
        .annotate(
            count=Count('id'),
            total=Sum('total')
        )
        .order_by('-total')
    )
    
    # Combinar métodos de pago
    payment_methods_combined = {}
    
    for pm in payment_methods_sales:
        payment_method = pm['payment_method']
        payment_methods_combined[payment_method] = {
            'count': pm['count'],
            'total': pm['total'],
            'source': 'Ventas'
        }
    
    for pm in payment_methods_orders:
        payment_method = pm['payment_method']
        if payment_method in payment_methods_combined:
            payment_methods_combined[payment_method]['count'] += pm['count']
            payment_methods_combined[payment_method]['total'] += pm['total']
            payment_methods_combined[payment_method]['source'] = 'Ambos'
        else:
            payment_methods_combined[payment_method] = {
                'count': pm['count'],
                'total': pm['total'],
                'source': 'Órdenes'
            }
    
    # Convertir a lista y ordenar por total
    payment_methods = [
        {
            'payment_method': k,
            'count': v['count'],
            'total': v['total'],
            'source': v['source']
        }
        for k, v in payment_methods_combined.items()
    ]
    payment_methods = sorted(payment_methods, key=lambda x: x['total'], reverse=True)[:5]
    
    # Productos más vendidos en ventas
    top_products_sales = SaleItem.objects.filter(
        sale__date__range=[start_date, end_date]
    ).values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('price'))
    ).order_by('-total_quantity')
    
    # Productos más vendidos en órdenes
    top_products_orders = OrderItem.objects.filter(
        order__date__range=[start_date, end_date]
    ).values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('price'))
    ).order_by('-total_quantity')
    
    # Combinar productos
    top_products_combined = {}
    
    for product in top_products_sales:
        name = product['product__name']
        top_products_combined[name] = {
            'total_quantity': product['total_quantity'],
            'total_revenue': product['total_revenue'],
            'source': 'Ventas'
        }
    
    for product in top_products_orders:
        name = product['product__name']
        if name in top_products_combined:
            top_products_combined[name]['total_quantity'] += product['total_quantity']
            top_products_combined[name]['total_revenue'] += product['total_revenue']
            top_products_combined[name]['source'] = 'Ambos'
        else:
            top_products_combined[name] = {
                'total_quantity': product['total_quantity'],
                'total_revenue': product['total_revenue'],
                'source': 'Órdenes'
            }
    
    # Convertir a lista y ordenar por cantidad
    top_products = [
        {
            'product__name': k,
            'total_quantity': v['total_quantity'],
            'total_revenue': v['total_revenue'],
            'source': v['source']
        }
        for k, v in top_products_combined.items()
    ]
    top_products = sorted(top_products, key=lambda x: x['total_quantity'], reverse=True)[:10]
    
    # Estado de órdenes
    order_status = (
        orders.values('status')
        .annotate(
            count=Count('id'),
            total=Sum('total')
        )
        .order_by('-count')
    )
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'sales': sales,
        'orders': orders,
        'total_sales': filtered_sales_count,
        'total_orders': filtered_orders_count,
        'total_transactions': total_transactions,
        'total_revenue': total_revenue,
        'sales_revenue': sales_revenue,
        'orders_revenue': orders_revenue,
        'payment_methods': payment_methods,
        'top_products': top_products,
        'order_status': order_status,
        'total_sales_count': total_sales_count,
        'total_orders_count': total_orders_count,
        'filtered_sales_count': filtered_sales_count,
        'filtered_orders_count': filtered_orders_count,
    }
    
    # Agregar mensajes de depuración
    messages.info(request, f"Rango de fechas: {start_date} - {end_date}")
    messages.info(request, f"Total de ventas en la base de datos: {total_sales_count}")
    messages.info(request, f"Total de órdenes en la base de datos: {total_orders_count}")
    messages.info(request, f"Ventas filtradas: {filtered_sales_count}")
    messages.info(request, f"Órdenes filtradas: {filtered_orders_count}")

    return render(request, 'admin_dashboard/reports/sales.html', context)
@login_required
@user_passes_test(is_admin)
def sales_report_excel(request):
    # Obtener el rango de fechas
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = timezone.make_aware(datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d'))
        end_date = timezone.make_aware(datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d'))
        end_date = end_date.replace(hour=23, minute=59, second=59)  # Ajustar al final del día

    # Crear el archivo Excel en memoria
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    
    # Hoja de ventas
    worksheet_sales = workbook.add_worksheet('Ventas')
    
    # Formatos - Corregidos para evitar el error 'set_color'
    title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
    header_format = workbook.add_format({'bold': True, 'bg_color': '#4e73df', 'font_color': 'white', 'align': 'center', 'valign': 'vcenter', 'border': 1})
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'align': 'center'})
    number_format = workbook.add_format({'num_format': '#,##0.00', 'align': 'right'})
    cell_format = workbook.add_format({'align': 'left', 'border': 1})

    # Título - Ventas
    worksheet_sales.merge_range('A1:F1', 'Reporte de Ventas', title_format)
    worksheet_sales.merge_range('A2:F2', f'Período: {start_date.strftime("%d/%m/%Y")} - {end_date.strftime("%d/%m/%Y")}', title_format)

    # Encabezados - Ventas
    headers_sales = ['ID Venta', 'Fecha', 'Cliente', 'Método de Pago', 'Total', 'Estado']
    for col, header in enumerate(headers_sales):
        worksheet_sales.write(3, col, header, header_format)

    # Datos - Ventas
    sales = Sale.objects.filter(date__range=[start_date, end_date]).order_by('date')
    row = 4
    for sale in sales:
        worksheet_sales.write(row, 0, sale.number, cell_format)
        worksheet_sales.write(row, 1, sale.date, date_format)
        worksheet_sales.write(row, 2, sale.customer_name, cell_format)
        worksheet_sales.write(row, 3, sale.get_payment_method_display(), cell_format)
        worksheet_sales.write(row, 4, float(sale.total), number_format)
        worksheet_sales.write(row, 5, 'Completada', cell_format)  # Las ventas siempre están completadas
        row += 1

    # Totales - Ventas
    total_row = row + 1
    worksheet_sales.write(total_row, 3, 'Total Ventas:', header_format)
    worksheet_sales.write_formula(total_row, 4, f'=SUM(E5:E{row})', number_format)
    
    # Hoja de órdenes
    worksheet_orders = workbook.add_worksheet('Órdenes')
    
    # Título - Órdenes
    worksheet_orders.merge_range('A1:G1', 'Reporte de Órdenes', title_format)
    worksheet_orders.merge_range('A2:G2', f'Período: {start_date.strftime("%d/%m/%Y")} - {end_date.strftime("%d/%m/%Y")}', title_format)

    # Encabezados - Órdenes
    headers_orders = ['Número', 'Fecha', 'Cliente', 'Método de Pago', 'Total', 'Estado', 'Tracking']
    for col, header in enumerate(headers_orders):
        worksheet_orders.write(3, col, header, header_format)

    # Datos - Órdenes
    orders = Order.objects.filter(date__range=[start_date, end_date]).order_by('date')
    row = 4
    for order in orders:
        worksheet_orders.write(row, 0, order.order_number, cell_format)
        worksheet_orders.write(row, 1, order.date, date_format)
        worksheet_orders.write(row, 2, order.fullname, cell_format)
        worksheet_orders.write(row, 3, order.get_payment_method_display(), cell_format)
        worksheet_orders.write(row, 4, float(order.total), number_format)
        worksheet_orders.write(row, 5, order.get_status_display(), cell_format)
        worksheet_orders.write(row, 6, order.tracking_number or 'N/A', cell_format)
        row += 1

    # Totales - Órdenes
    total_row = row + 1
    worksheet_orders.write(total_row, 3, 'Total Órdenes:', header_format)
    worksheet_orders.write_formula(total_row, 4, f'=SUM(E5:E{row})', number_format)
    
    # Hoja de resumen
    worksheet_summary = workbook.add_worksheet('Resumen')
    
    # Título - Resumen
    worksheet_summary.merge_range('A1:D1', 'Resumen de Ventas y Órdenes', title_format)
    worksheet_summary.merge_range('A2:D2', f'Período: {start_date.strftime("%d/%m/%Y")} - {end_date.strftime("%d/%m/%Y")}', title_format)
    
    # Datos de resumen
    sales_count = sales.count()
    sales_total = sales.aggregate(total=Sum('total'))['total'] or 0
    orders_count = orders.count()
    # Solo contar órdenes completadas para el total
    completed_orders_total = orders.filter(status='completed').aggregate(total=Sum('total'))['total'] or 0
    
    # Encabezados - Resumen
    worksheet_summary.write(4, 0, 'Tipo', header_format)
    worksheet_summary.write(4, 1, 'Cantidad', header_format)
    worksheet_summary.write(4, 2, 'Total', header_format)
    
    # Datos - Resumen
    worksheet_summary.write(5, 0, 'Ventas', cell_format)
    worksheet_summary.write(5, 1, sales_count, cell_format)
    worksheet_summary.write(5, 2, float(sales_total), number_format)
    
    worksheet_summary.write(6, 0, 'Órdenes (Completadas)', cell_format)
    worksheet_summary.write(6, 1, orders_count, cell_format)
    worksheet_summary.write(6, 2, float(completed_orders_total), number_format)
    
    worksheet_summary.write(7, 0, 'Total', header_format)
    worksheet_summary.write(7, 1, sales_count + orders_count, header_format)
    worksheet_summary.write(7, 2, float(sales_total + completed_orders_total), number_format)
    
    # Ajustar anchos de columna
    for worksheet in [worksheet_sales, worksheet_orders, worksheet_summary]:
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 30)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 20)

    workbook.close()
    output.seek(0)

    # Generar la respuesta HTTP
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=reporte_combinado_{timezone.now().strftime("%Y%m%d")}.xlsx'
    
    return response

@login_required
@user_passes_test(is_admin)
def sales_report_pdf(request):
    # Importar las clases necesarias de reportlab
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    
    # Obtener el rango de fechas
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = timezone.make_aware(datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d'))
        end_date = timezone.make_aware(datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d'))
        end_date = end_date.replace(hour=23, minute=59, second=59)  # Ajustar al final del día

    # Crear el archivo PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Obtener estilos
    styles = getSampleStyleSheet()

    # Estilos para tablas
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4e73df')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
    ])

    # Datos de ventas
    sales = Sale.objects.filter(date__range=[start_date, end_date]).order_by('date')
    sales_data = [['ID', 'Fecha', 'Cliente', 'Método de Pago', 'Total', 'Estado']]
    
    for sale in sales:
        sales_data.append([
            str(sale.number),
            sale.date.strftime('%d/%m/%Y'),
            sale.customer_name,
            sale.get_payment_method_display(),
            f'${sale.total:,.2f}',
            'Completada'
        ])

    # Datos de órdenes
    orders = Order.objects.filter(date__range=[start_date, end_date]).order_by('date')
    orders_data = [['Número', 'Fecha', 'Cliente', 'Método de Pago', 'Total', 'Estado']]
    
    for order in orders:
        orders_data.append([
            str(order.order_number),
            order.date.strftime('%d/%m/%Y'),
            order.fullname,
            order.get_payment_method_display(),
            f'${order.total:,.2f}',
            order.get_status_display()
        ])

    # Crear tablas
    sales_table = Table(sales_data)
    sales_table.setStyle(table_style)
    
    orders_table = Table(orders_data)
    orders_table.setStyle(table_style)
    
    # Agregar elementos al PDF
    elements.append(Paragraph(f"Reporte de Ventas y Órdenes", styles['Title']))
    elements.append(Paragraph(f"Período: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("Ventas", styles['Heading2']))
    elements.append(sales_table)
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("Órdenes", styles['Heading2']))
    elements.append(orders_table)

    # Generar PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    # Generar la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=reporte_combinado_{timezone.now().strftime("%Y%m%d")}.pdf'
    response.write(pdf)

    return response




@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            product.delete()
            messages.success(request, 'Producto eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el producto: {str(e)}')
    return redirect('admin_product_list')
@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    # Buscar o crear la categoría "Sin Categoría"
    uncategorized, created = Category.objects.get_or_create(
        name="Sin Categoría", 
        defaults={"description": "Productos sin categoría asignada"}
    )

    if request.method == 'POST':
        try:
            # Mover los productos a la categoría "Sin Categoría"
            products_moved = category.product_set.update(category=uncategorized)
            
            # Eliminar la categoría
            category.delete()
            
            if products_moved:
                messages.success(request, f'{products_moved} producto(s) fueron movidos a "Sin Categoría".')
            messages.success(request, f'Categoría "{category.name}" eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar la categoría: {str(e)}')
    
    return redirect('admin_category_list')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category

def delete_all_categories(request):
    # Verifica que el usuario tenga permisos para eliminar categorías
    if request.method == 'POST':
        Category.objects.exclude(name="Sin Categoría").delete()  # Elimina todas menos "Sin Categoría"
        return redirect('admin_category_list')  # Redirige a la lista de categorías
    return render(request, 'admin_dashboard/confirm_delete_all.html')  # Página de confirmación si no es un POST


from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import redirect
from django.db import transaction
from django.core.management import call_command

@login_required
@user_passes_test(lambda u: u.is_superuser)  # Solo superusuarios pueden acceder
def reset_database(request):
    if request.method == 'POST':
        confirmation = request.POST.get('confirmation')
        if confirmation == 'RESET':
            try:
                with transaction.atomic():
                    # Guardar usuarios admin
                    admin_users = User.objects.filter(is_staff=True).values_list('id', flat=True)
                    
                    # Limpiar todas las tablas excepto auth
                    Sale.objects.all().delete()
                    SaleItem.objects.all().delete()
                    Product.objects.all().delete()
                    Category.objects.all().delete()
                    CustomUser.objects.all().delete()
                    Company.objects.all().delete()
                    Certification.objects.all().delete()
                    
                    # Restaurar datos iniciales si existen fixtures
                    try:
                        call_command('loaddata', 'initial_data')
                    except:
                        pass

                    messages.success(request, 'Base de datos reiniciada exitosamente.')
                    return redirect('admin_dashboard')
            except Exception as e:
                messages.error(request, f'Error al reiniciar la base de datos: {str(e)}')
        else:
            messages.error(request, 'Código de confirmación incorrecto.')
    
    return render(request, 'admin_dashboard/reset_database.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def backup_database(request):
    try:
        # Crear un archivo temporal para el backup
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f'backup_{timestamp}.json'
        
        # Usar StringIO para capturar la salida del comando dumpdata
        output = StringIO()
        call_command('dumpdata', 
                    exclude=['auth.permission', 'contenttypes', 'admin.logentry', 'sessions'],
                    indent=2,
                    stdout=output)
        
        # Crear la respuesta HTTP con el archivo
        response = HttpResponse(output.getvalue(), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error al crear el backup: {str(e)}')
        return redirect('admin_dashboard')
 

@login_required
@permission_required('app.delete_sale')
def delete_sale(request, sale_id):
    if request.method == 'POST':
        try:
            sale = Sale.objects.get(id=sale_id)
            sale_id = sale.id  # Guardar ID para mensaje
            sale.delete()
            messages.success(request, f'Venta #{sale_id} eliminada correctamente.')
        except Sale.DoesNotExist:
            messages.error(request, 'La venta no existe.')
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('admin_sales_report')))

@login_required
@permission_required('app.delete_sale')
def delete_selected_sales(request):
    if request.method == 'POST':
        selected_ids = request.POST.get('selected_ids', '')
        if selected_ids:
            ids = [int(x) for x in selected_ids.split(',')]
            deleted_count = Sale.objects.filter(id__in=ids).delete()[0]
            messages.success(request, f'{deleted_count} ventas eliminadas correctamente.')
        else:
            messages.warning(request, 'No se seleccionaron ventas para eliminar.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('admin_sales_report')))


@login_required
@permission_required('app.delete_sale')
def delete_all_sales(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Convertir las fechas a objetos aware
        if start_date:
            start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date:
            end_date = timezone.make_aware(datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
        
        # Filtrar por fechas si se proporcionan
        query = Sale.objects
        if start_date:
            query = query.filter(date__gte=start_date)
        if end_date:
            query = query.filter(date__lte=end_date)
            
        deleted_count = query.delete()[0]
        messages.success(request, f'{deleted_count} ventas eliminadas correctamente.')
    
    return redirect('admin_sales_report')


def admin_print_product_labels(request):
    """Vista para imprimir etiquetas de productos."""
    products = Product.objects.filter(is_available=True).order_by('name')
    return render(request, 'admin_dashboard/print_labels.html', {'products': products})

from django.shortcuts import render, redirect
from .forms import BrandForm
from .models import Brand

def manage_brands(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_brands')  # Redirige a la misma página para ver la marca agregada
    else:
        form = BrandForm()
    
    brands = Brand.objects.all()
    return render(request, 'admin_dashboard/products/manage_brands.html', {'form': form, 'brands': brands})

def edit_brand(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('manage_brands')  # Redirige a la página de administración de marcas
    else:
        form = BrandForm(instance=brand)

    return render(request, 'admin_dashboard/products/manage_brands.html', {'form': form, 'brand': brand})

def delete_brand(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    if request.method == 'POST':
        brand.delete()
        return redirect('manage_brands')  # Redirige a la misma página después de eliminar

    return render(request, 'admin_dashboard/products/confirm_delete.html', {'brand': brand})
def associate_certification(request, cert_id):
    # Obtén la certificación por su ID
    certification = get_object_or_404(Certification, id=cert_id)
    company = Company.objects.first()  # Obtener la primera empresa, puedes cambiar esto si es necesario
    
    if certification not in company.certifications.all():
        company.certifications.add(certification)
        messages.success(request, "Certificación asociada correctamente.")
    else:
        messages.warning(request, "La certificación ya está asociada a esta empresa.")
    
    return redirect('admin_company_detail')




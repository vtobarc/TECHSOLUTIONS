from datetime import timezone
from urllib import request
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random
import string
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import qrcode
from PIL import Image
from django.conf import settings
from decimal import Decimal
from tinymce.models import HTMLField
from django.db import models
from django.db.models import Sum, F
from cloudinary.models import CloudinaryField
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.uploader import upload
from django.core.files.base import File
import random
import string
from io import BytesIO
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.conf import settings
from django.db import models
from PIL import Image
import imghdr
import barcode
from barcode.writer import ImageWriter
import qrcode


User = settings.AUTH_USER_MODEL

def validate_image(image):
    if image.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("El archivo es demasiado grande (Máximo 5MB)")
    if not image.content_type.startswith("image/"):
        raise ValidationError("Solo se permiten imágenes")
    
class CustomUser(AbstractUser):
    """Modelo de usuario personalizado basado en AbstractUser."""
    # Datos personales
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)  # Permitir nulo y duplicados    
    cedula = models.CharField(max_length=20, validators=[RegexValidator(r'^\d+$', 'Ingrese un número de cédula válido.')], blank=True, null=True)
    email = models.EmailField(unique=True)  # Ensure email is unique
    USERNAME_FIELD = 'email'  # Set email as the login field
    REQUIRED_FIELDS = ['cedula']  # Add any required fields
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=10, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')], blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    
    # Información de contacto
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Ingrese un número de teléfono válido.')])
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    idioma_preferido = models.CharField(max_length=10, choices=[('es', 'Español'), ('en', 'Inglés')], default='es')
    
    # Información profesional
    titulo_profesional = models.CharField(max_length=100, blank=True, null=True)
    habilidades_tecnicas = models.TextField(blank=True, null=True)
    habilidades_blandas = models.TextField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    
    # Rol y estado
    rol = models.CharField(max_length=50, choices=[('Usuario', 'Usuario'), ('Servidor', 'Servidor'), ('Admin', 'Admin')], default='Usuario')
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    suspension_reason = models.CharField(max_length=255, blank=True, null=True)
    
    # Seguimiento y actividad
    foto_perfil = CloudinaryField('imagen', folder='perfil/', blank=True, null=True, default='default_profile.jpg')
    cover_photo = CloudinaryField('imagen', folder='cover_photos/', blank=True, null=True, default='default_cover.jpg')
    last_activity = models.DateTimeField(auto_now=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    ip_registro = models.GenericIPAddressField(blank=True, null=True)
    
    # Evaluación y reputación
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], help_text="Calificación de usuario entre 0 y 5 estrellas")
    num_ratings = models.IntegerField(default=0)
    
    # Preferencias
    dark_mode = models.BooleanField(default=False)
    preferencias = models.JSONField(default=dict, blank=True)
    
    # Relaciones
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='customuser_groups', related_query_name='user')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='customuser_permissions', related_query_name='user')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.username} - {self.cedula}"
    
    def is_online(self):
        """Devuelve True si el usuario está en línea."""
        if self.last_login_time and (not self.last_logout_time or self.last_login_time > self.last_logout_time):
            return True
        return False

    def formatted_last_activity(self):
        from django.utils.timezone import now
        from django.contrib.humanize.templatetags.humanize import naturaltime
        if self.is_online():
            return "En línea ahora"
        return f"Última conexión: {naturaltime(self.last_login_time) if self.last_login_time else 'Nunca'}"

    
    def update_average_rating(self):
        ratings = self.ratings_received.all()
        self.num_ratings = ratings.count()
        self.rating = round(sum(r.score for r in ratings) / self.num_ratings, 2) if self.num_ratings else 0.0
        self.save()

from django.db import models

class Company(models.Model):
    
    # Información básica
    name = models.CharField(max_length=255)
    ruc = models.CharField(max_length=13, unique=True)  # Identificación fiscal
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    logo = CloudinaryField('imagen', folder='company_logos/', blank=True, null=True)
    image = CloudinaryField('imagen', folder='company_images/', blank=True, null=True)

    # Información adicional
    mission = models.TextField(blank=True, null=True)  
    vision = models.TextField(blank=True, null=True)   
    values = models.TextField(blank=True, null=True)   
    history = models.TextField(blank=True, null=True)  
    slogan = models.CharField(max_length=255, blank=True, null=True)  
    founded_date = models.DateField(blank=True, null=True)  

    # Información financiera y legal
    legal_representative = models.CharField(max_length=255, blank=True, null=True)  
    capital = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  
    employees_count = models.PositiveIntegerField(blank=True, null=True)  

    # Redes sociales
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    # Horario de atención
    opening_hours = models.CharField(max_length=255, blank=True, null=True)

    # Ubicación
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Datos comerciales
    industry = models.CharField(max_length=255, blank=True, null=True)  # Sector empresarial
    services = models.TextField(blank=True, null=True)  # Lista de servicios ofrecidos
    
    # Relación ManyToMany con el modelo de certificaciones
# Relación ManyToMany con el modelo de certificaciones
    certifications = models.ManyToManyField('Certification', related_name='companies', blank=True)

    branches_count = models.PositiveIntegerField(default=1)  # Cantidad de sucursales

    # Equipo colaborativo (Relación con un modelo de empleados)
    employees = models.ManyToManyField('Employee', related_name='companies', blank=True)

    def __str__(self):
        return self.name
class Certification(models.Model):
    name_certification = models.CharField(max_length=255)
    logos = CloudinaryField('imagen', folder='certifications/', blank=True, null=True)
    expiry_date = models.DateField(null=True, blank=True)  # Campo de expiración

    def __str__(self):
        return self.name_certification


class Employee(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = CloudinaryField('imagen', folder='employees/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.position}"


    
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institucion = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    descripcion = models.TextField()

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_tarjeta = models.CharField(max_length=50)
    numero_tarjeta = models.CharField(max_length=16)



class ActiveSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='active_sessions')
    device = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=255, unique=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.device} ({self.ip_address})"

class NotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Notificaciones de {self.user.username}"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username if self.user else 'Usuario desconocido'} - {self.action}"
class ActivityMessage(models.Model):
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
  










def validate_image(image):
    # Verificar si la imagen tiene atributo `file.content_type`
    if hasattr(image, 'file') and hasattr(image.file, 'content_type'):
        content_type = image.file.content_type
    else:
        format = imghdr.what(image)
        if format:
            content_type = f'image/{format}'
        else:
            raise ValidationError("Formato de imagen no válido.")

    valid_types = ['image/jpeg', 'image/png', 'image/gif']
    if content_type not in valid_types:
        raise ValidationError("Formato de imagen no permitido. Usa JPG, PNG o GIF.")

    # Verificar dimensiones si es necesario
    try:
        img = Image.open(image)
        if img.width > 5000 or img.height > 5000:
            raise ValidationError("La imagen es demasiado grande (máx: 5000x5000px).")
    except Exception:
        raise ValidationError("No se pudo procesar la imagen. Asegúrate de que es válida.")



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name if not self.parent else f"{self.parent} -> {self.name}"

    class Meta:
        verbose_name_plural = "Categories"

    def product_count(self):
        return self.product_set.count()

    def total_stock(self):
        return self.product_set.aggregate(total_stock=Sum('stock'))['total_stock'] or 0

    def total_value(self):
        return self.product_set.aggregate(total_value=Sum(F('stock') * F('price')))['total_value'] or 0

    def get_subcategories(self):
        return self.subcategories.all()  # Obtiene todas las subcategorías

def generate_unique_code(length=12):
    return ''.join(random.choices(string.digits, k=length))
from django.core.files.base import File  # Importa File aquí
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
import qrcode
from cloudinary.uploader import upload
class Product(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = HTMLField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', validators=[validate_image], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    brand = models.CharField(max_length=200, blank=True)
    features = models.TextField(blank=True, help_text="List the features of the product, separated by commas or as a formatted text.")
    color = models.CharField(max_length=100, blank=True, help_text="Color of the product (e.g., Red, Blue, Black, #FFFFFF).")
    
    def __str__(self):
        return f"{self.name} - {self.code}"
    
    def save(self, *args, **kwargs):
        if not self.barcode and self.code:
            barcode_value = self.code.zfill(12)
            ean = barcode.get('ean13', barcode_value, writer=ImageWriter())
            buffer = BytesIO()
            ean.write(buffer)
            self.barcode_image.save(f'barcode_{self.code}.png', File(buffer), save=False)
            self.barcode = ean.get_fullcode()

            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.code)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            self.qr_code.save(f'qr_{self.code}.png', File(buffer), save=False)

        super().save(*args, **kwargs)
    
    def get_main_image(self):
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image.image
        return self.image  # Fallback to the original image field
        
    def get_gallery_images(self):
        return self.images.all()

    
    
# Add this new model to your models.py file
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/', validators=[validate_image])
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        
    def __str__(self):
        return f"Image for {self.product.name} ({self.id})"
    
    def save(self, *args, **kwargs):
        # If this is marked as main image, unmark others
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)
        # If this is the first image, make it the main image
        elif not ProductImage.objects.filter(product=self.product).exists():
            self.is_main = True
        super().save(*args, **kwargs) 
        
class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        """El stock ya se modifica en `create_sale`, aquí solo registramos el movimiento"""
        super().save(*args, **kwargs)


class Sale(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Efectivo'),
        ('CARD', 'Tarjeta'),
        ('TRANSFER', 'Transferencia'),
    ]
    
    number = models.CharField(max_length=10, unique=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=200, blank=True)
    customer_id = models.CharField(max_length=20, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='CASH')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def generate_number(self):
        """Generar número de venta único."""
        if not self.number:
            last_sale = type(self).objects.order_by('-id').first()
            last_number = int(last_sale.number[4:]) if last_sale else 0
            self.number = f'VTA-{str(last_number + 1).zfill(6)}'
    
    def update_totals(self):
        """Actualizar totales de la venta."""
        self.subtotal = sum(item.subtotal for item in self.items.all())
        self.tax = self.subtotal * Decimal('0.15')
        self.total = self.subtotal + self.tax
        type(self).objects.filter(pk=self.pk).update(
            subtotal=self.subtotal,
            tax=self.tax,
            total=self.total
        )

    def create_stock_movements(self):
        """Crear movimientos de stock para cada producto vendido."""
        for item in self.items.all():
            StockMovement.objects.create(
                product=item.product,
                movement_type='OUT',
                quantity=item.quantity,
                notes=f"Venta {self.number}"
            )

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.generate_number()
            super().save(*args, **kwargs)
            self.create_stock_movements()  # 🔥 Aquí es donde se crean los movimientos de stock


from django.db import transaction

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """Validar stock pero no modificarlo aquí"""
        if self.product.stock < self.quantity:
            raise ValidationError(f"No hay suficiente stock para {self.product.name}.")

        self.subtotal = self.quantity * self.price

        with transaction.atomic():
            super().save(*args, **kwargs)
            self.sale.update_totals()
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_uncategorized_category(sender, **kwargs):
    if sender.name == 'dynamics':  # Reemplaza 'tu_app' con el nombre de tu app
        Category.objects.get_or_create(name="Sin Categoría", defaults={"description": "Productos sin categoría asignada"})



class Quote(models.Model):
    quote_number = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=200)
    customer_id = models.CharField(max_length=20, blank=True)  # RUC/Cedula
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    validity_days = models.IntegerField(default=15)  # Validez de la cotización en días
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_converted = models.BooleanField(default=False)  # Si se convirtió en venta

    def __str__(self):
        return f"Quote #{self.quote_number}"

    def save(self, *args, **kwargs):
        if not self.quote_number:
            # Generar número de cotización: Q + timestamp
            self.quote_number = 'Q' + timezone.now().strftime('%Y%m%d%H%M%S')
        super().save(*args, **kwargs)

class QuoteItem(models.Model):
    quote = models.ForeignKey(Quote, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)  # Cambiar a SET_NULL
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"




def generate_order_number():
    return str(uuid.uuid4())[:20]  # Genera un identificador único basado en UUID

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completado'),
        ('canceled', 'Cancelado'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date = models.DateTimeField(auto_now_add=True)

    # Datos de entrega con valores por defecto
    email = models.EmailField(default='example@example.com')
    phone = models.CharField(max_length=15, default='0000000000')
    fullname = models.CharField(max_length=255, default='Nombre Desconocido')
    address = models.TextField(default='Sin dirección')
    city = models.CharField(max_length=100, default='Ciudad Desconocida')
    postal_code = models.CharField(max_length=10, default='00000')
    state = models.CharField(max_length=100, default='Estado Desconocido')
    payment_method = models.CharField(max_length=50, default='Desconocido')

    def __str__(self):
        return f'Pedido {self.order_number} - {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} unidades"

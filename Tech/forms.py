import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Certification, Company, CustomUser, ProductImage
from django.core.validators import RegexValidator
from django import forms
from .models import CustomUser, Education, Experience, PaymentMethod
from django.core.exceptions import ValidationError
import magic
from django import forms
from .models import Product, Category, StockMovement
from tinymce.widgets import TinyMCE

class CustomUserCreationForm(UserCreationForm):
    cedula = forms.CharField(
        max_length=20, 
        required=True, 
        validators=[RegexValidator(r'^\d{10}$', 'Cédula debe ser un número de 10 dígitos')]
    )

    class Meta:
        model = CustomUser
        fields = ('cedula', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.username:  # Si username está vacío, generamos uno basado en el email
            user.username = user.email.split('@')[0]  # Usa la parte antes del @ como username
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['cedula', 'first_name', 'last_name', 'email', 
                  'telefono', 'direccion', 'ciudad', 'provincia', 'pais', 'fecha_nacimiento', 
                  'genero', 'idioma_preferido', 'titulo_profesional', 'biografia', 'linkedin_url', 
                  'github_url', 'portfolio_url', 'habilidades_tecnicas', 'habilidades_blandas']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'biografia': forms.Textarea(attrs={'rows': 4}),
            'habilidades_tecnicas': forms.Textarea(attrs={'rows': 3}),
            'habilidades_blandas': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if cedula and not cedula.isdigit():
            raise forms.ValidationError("La cédula debe contener solo números.")
        return cedula

    # Añade más métodos de limpieza y validación según sea necesario
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institucion', 'titulo', 'fecha_inicio', 'fecha_fin']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['empresa', 'cargo', 'fecha_inicio', 'fecha_fin', 'descripcion']

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['tipo_tarjeta', 'numero_tarjeta']

import random
from django.core.exceptions import ValidationError
from barcode import get_barcode_class
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File



class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_main', 'order']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0})
        }



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'barcode', 'category', 'description', 'price', 
                   'stock', 'minimum_stock', 'image', 'tax', 'discount', 'brand', 'features', 'color']
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 20}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Características del producto separa con "," coma cada una'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color del producto'})        
            }

    # Campo 'code' no obligatorio
    code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Se generará automáticamente si no se ingresa'})
    )

    # Método para generar el código automáticamente si no se ha ingresado
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code:
            # Generar un código único numérico
            code = self.generate_unique_numeric_code()
        return code

    def generate_unique_numeric_code(self):
        while True:
            # Generar un código numérico aleatorio de 12 dígitos (puedes ajustarlo según tus necesidades)
            code = ''.join(random.choices('0123456789', k=12))  # Código numérico de 12 caracteres
            if not Product.objects.filter(code=code).exists():  # Verificar si el código ya existe
                break
        return code
    def clean_color(self):
        color = self.cleaned_data.get('color')
        
        # Validación de color hexadecimal (ejemplo: #ff6347)
        hex_color_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
        
        # Validación de color por nombre (opcional)
        valid_colors = ['red', 'blue', 'green', 'yellow', 'black', 'white', 'gray', 'orange', 'purple', 'pink']
        
        if not hex_color_pattern.match(color) and color.lower() not in valid_colors:
            raise ValidationError(f"El color '{color}' no es válido. Usa un color válido como: rojo, azul, #ff6347, etc.")
        
        return color

    # Asegúrate de generar el código de barras y QR solo si es necesario
    def save(self, commit=True):
        # Si el código está vacío, generarlo antes de guardar
        if not self.instance.code:
            self.instance.code = self.generate_unique_numeric_code()

        # Generar el código de barras y QR
        if not self.instance.barcode:
            barcode_value = self.instance.code
            ean = get_barcode_class('ean13')(barcode_value, writer=ImageWriter())
            buffer = BytesIO()
            ean.write(buffer)
            self.instance.barcode_image.save(f'barcode_{self.instance.code}.png', File(buffer), save=False)
            self.instance.barcode = ean.get_fullcode()

        if not self.instance.qr_code:
            import qrcode
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.instance.code)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            self.instance.qr_code.save(f'qr_{self.instance.code}.png', File(buffer), save=False)

        return super().save(commit=commit)

    

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2})
        }
# inventory/forms.py (Agregar el CategoryForm)
from django import forms
from .models import Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'icon', 'is_active', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la categoría'
            }),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name__iexact=name).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Ya existe una categoría con este nombre.')
        return name


# forms.py - Update your CompanyForm
from django import forms
from .models import Company, Certification

class CompanyForm(forms.ModelForm):
    certifications = forms.ModelMultipleChoiceField(
        queryset=Certification.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Company
        fields = [
            'name', 'ruc', 'address', 'phone', 'email', 'website', 'logo', 'image',
            'mission', 'vision', 'values', 'history', 'slogan', 'founded_date',
            'legal_representative', 'capital', 'employees_count',
            'facebook', 'twitter', 'linkedin', 'instagram', 'youtube', 'opening_hours',
            'country', 'city', 'latitude', 'longitude', 'industry', 'services', 'branches_count',
            'certifications'
        ]
        # Only make the truly required fields required in the form
        required = ['name', 'ruc', 'address', 'phone', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields not required except those in the required list
        for field_name, field in self.fields.items():
            if field_name not in self.Meta.required:
                field.required = False
class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name_certification', 'logos']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make logos field not required
        self.fields['logos'].required = False



from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'email', 'phone', 'profile_picture']

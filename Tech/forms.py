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
from django.contrib.auth.decorators import login_required
import random
import re
from django.core.exceptions import ValidationError
from django import forms
from django.db import transaction
from barcode import get_barcode_class
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile, File  # Asegúrate de agregar 'File' aquí
from .models import Product, ProductImage, Category, StockMovement
from tinymce.widgets import TinyMCE
from .models import Brand

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
import re
from django.core.exceptions import ValidationError
from django import forms
from django.db import transaction
from barcode import get_barcode_class
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile
from .models import Product, ProductImage, Category, StockMovement
from tinymce.widgets import TinyMCE

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_main', 'order']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0})
        }

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'logo', 'website']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la marca'}),
            'logo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Sitio web (opcional)'}),
        }
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'category', 'description', 'price', 
                  'stock', 'minimum_stock', 'image', 'tax', 'discount', 'brand', 'features', 'color']
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 20}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Características del producto separa con "," coma cada una'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color del producto'})        
        }
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False)

    # Campo 'code' no obligatorio
    code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Se generará automáticamente si no se ingresa'})
    )
    
    def clean_color(self):
        color = self.cleaned_data.get('color')
        if not color:
            return color
            
        # Validación de color hexadecimal (ejemplo: #ff6347)
        hex_color_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
        
        # Validación de color por nombre (opcional)
        valid_colors = ['red', 'blue', 'green', 'yellow', 'black', 'white', 'gray', 'orange', 'purple', 'pink']
        
        if not hex_color_pattern.match(color) and color.lower() not in valid_colors:
            raise ValidationError(f"El color '{color}' no es válido. Usa un color válido como: rojo, azul, #ff6347, etc.")
        
        return color



class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2})
        }

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
    # Definición del campo account_type con opciones de selección
    ACCOUNT_TYPE_CHOICES = [
        ('Ahorro', 'Ahorro'),
        ('Corriente', 'Corriente'),
    ]
    
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE_CHOICES,
        widget=forms.Select,
        required=False  # Puedes cambiar a True si deseas que sea obligatorio
    )
    
    certifications = forms.ModelMultipleChoiceField(
        queryset=Certification.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    # Definir branchesfijos con TinyMCE (Fuera de Meta)
    branchesfijos = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 20}),
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
            'certifications', 'account_number', 'account_name', 'bank_name', 'account_type', 'swift_code', 'iban', 'branchesfijos'
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

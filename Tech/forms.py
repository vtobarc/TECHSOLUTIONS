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
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # First save the product to get a valid instance with ID
                    product = form.save()
                    
                    # Now that we have a saved product with an ID, create the formset
                    formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
                    
                    if formset.is_valid():
                        # Process the formset
                        formset_instances = formset.save(commit=False)
                        
                        # Explicitly set the product for each instance and save
                        for instance in formset_instances:
                            instance.product = product  # This is crucial
                            instance.save()
                        
                        # Handle deleted objects
                        for obj in formset.deleted_objects:
                            obj.delete()
                        
                        # Ensure there's a main image if any images exist
                        if not ProductImage.objects.filter(product=product, is_main=True).exists() and \
                           ProductImage.objects.filter(product=product).exists():
                            first_image = ProductImage.objects.filter(product=product).first()
                            first_image.is_main = True
                            first_image.save()
                        
                        messages.success(request, f"Producto {'actualizado' if product_id else 'creado'} correctamente.")
                        return redirect('admin_product_list')
                    else:
                        # Log formset errors for debugging
                        logger.error(f"Formset validation errors: {formset.errors}")
                        for error in formset.non_form_errors():
                            logger.error(f"Non-form error: {error}")
                        
                        # Raise an exception to trigger rollback
                        raise ValidationError("Error en el formulario de imágenes")
            except ValidationError as ve:
                messages.error(request, f"Error de validación: {str(ve)}")
            except Exception as e:
                logger.error(f"Error al {'actualizar' if product_id else 'crear'} el producto: {str(e)}")
                messages.error(request, f"Error al {'actualizar' if product_id else 'crear'} el producto: {str(e)}")
        else:
            # Form is invalid, create formset for rendering
            formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
    else:
        # GET request
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

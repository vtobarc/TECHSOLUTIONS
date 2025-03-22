from filecmp import clear_cache
from django.urls import path
from .views import add_to_cart, base_product, category_detail, checkout, cliente_home, create_quote, delete_category,  get_products, home_view, nosotros_view, product_detail, quote_pdf, quote_to_sale, servicios
from .views import cliente_home
from django.contrib.auth import views as auth_views
from .views import register_view  # Importa la vista de registro
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import add_to_cart, cart_detail, remove_from_cart
from .views import (
    home_view, nosotros_view, servicios, category_detail, product_detail, 
    get_products, add_to_cart, cart_detail, remove_from_cart, base_product, 
    create_quote, quote_pdf, quote_to_sale, register_view, cliente_home
)

urlpatterns = [
    
    path('', home_view, name='home'),  # La URL de la página de inicio
    path('login/', auth_views.LoginView.as_view(template_name='login_and_signup/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', register_view, name='signup'),  # Ruta para el registro
    path('perfil/', views.perfil, name='perfil'),
    path('profile/', views.profile_view, name='profile'),
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('update_cover_photo/', views.update_cover_photo, name='update_cover_photo'),
    path('update_profile_field/', views.update_profile_field, name='update_profile_field'),
    path('add_education/', views.add_education, name='add_education'),
    path('update_education/<int:education_id>/', views.update_education, name='update_education'),
    path('delete_education/<int:education_id>/', views.delete_education, name='delete_education'),
    path('add_experience/', views.add_experience, name='add_experience'),
    path('update_experience/<int:experience_id>/', views.update_experience, name='update_experience'),
    path('delete_experience/<int:experience_id>/', views.delete_experience, name='delete_experience'),
    path('add_payment_method/', views.add_payment_method, name='add_payment_method'),
    path('update_payment_method/<int:payment_method_id>/', views.update_payment_method, name='update_payment_method'),
    path('delete_payment_method/<int:payment_method_id>/', views.delete_payment_method, name='delete_payment_method'),
    path('update_dark_mode/', views.update_dark_mode, name='update_dark_mode'),
    path('update_notification_settings/', views.update_notification_settings, name='update_notification_settings'),
    path('cliente/', cliente_home, name='cliente_home'),
    path('nosotros/', nosotros_view, name='nosotros'),
    path('servicios/', servicios, name='servicios'),
    path('products/', views.product_list, name='product_list'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('product/image/<int:image_id>/delete/', views.delete_product_image, name='delete_product_image'),
    path('product/image/<int:image_id>/set-main/', views.set_main_image, name='set_main_image'),
    path('export/', views.export_products, name='export_products'),
    path('print-labels/', views.print_labels, name='print_labels'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('categories/', views.category_list, name='category_list'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('delete_category/<int:pk>/', delete_category, name='delete_category'),

    path('reports/', views.reports, name='reports'),
    path('pos/', views.pos_view, name='pos'),
    path('pos/get-product/', views.get_product_by_code, name='get_product_by_code'),  # Changed URL pattern
    path('inventory/pos/products/', get_products, name='get_products'),
    path('pos/products/', views.get_products, name='pos_products'),
    path('pos/product/', views.get_product_by_code, name='get_product_by_code'),
    path('pos/create-sale/', views.create_sale, name='create_sale'),
    path('products/', views.get_products, name='get_products'),
    path('product/', views.get_product_by_code, name='get_product_by_code'),
    path('create-sale/', views.create_sale, name='create_sale'),
    path('inventory/receipt/<str:sale_number>/', views.get_receipt, name='get_receipt'),
    path('company/', views.company_detail, name='company_detail'),
    path('inventory/product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('sales-history/', views.sales_history, name='sales_history'),
    path('invoice/<int:id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/receipt/<str:sale_number>/', views.get_receipt, name='get_receipt'),
    path('pos/create-quote/', create_quote, name='create_quote'),
    path('pos/quote-to-sale/<str:quote_number>/', quote_to_sale, name='quote_to_sale'),
    path('pos/quote-pdf/<str:quote_number>/', quote_pdf, name='quote_pdf'),
    path('edit_certification/<int:id>/', views.edit_certification, name='edit_certification'),
    path('delete_certification/<int:id>/', views.delete_certification, name='delete_certification'),
    path('categoria/<int:category_id>/producto/<int:product_id>/', category_detail, name='product_detail'),
    path('categoria/<int:category_id>/producto/<int:product_id>/', views.category_detail, name='category_detail'),
    path('producto/<int:product_id>/', views.product_detail, name='product_detail'),
    path('categoria/<int:category_id>/', views.category_detail, name='category_detail'),
    path('categoria/<int:category_id>/', category_detail, name='category_detail'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/data/', views.cart_data, name='cart_data'),
    
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),  # Agregar producto
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),  # Eliminar un producto
    path('cart/clear/', views.clear_cart, name='clear_cart'),  # Vaciar carrito
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),  # Eliminar un producto
      # Vistas del carrito
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/data/', views.cart_data, name='cart_data'),
    
    # Vistas de checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.process_order, name='process_order'),
    path('order/success/', views.order_success, name='order_success'),
    path('order/success/<str:order_id>/', views.order_success, name='order_success_with_id'),
    path('orders/', views.view_orders, name='view_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('orders/<int:order_id>/tracking/', views.add_tracking, name='add_tracking'),
    path('orders/<int:order_id>/print/', views.print_invoice, name='print_invoice'),
    path('process-order/', views.process_order, name='process_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('checkout/', views.checkout, name='checkout'),

    
    
    path("categoria/", base_product, name="all_categories"),  # Muestra todas las categorías
    path("categoria/<int:category_id>/", base_product, name="category_detail"),  # Filtra por categoría específica
    path('producto/<int:product_id>/', views.product_detail, name='product_detail'),
    path('categoria/<int:category_id>/producto/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cliente/producto/<int:product_id>/', views.cliente_home, name='cliente_product_detail'),
    
    
    path('prueba/', views.prueba, name='prueba'),
    
    
    
    path('ver-pedidos/', views.view_orders, name='view_orders'),
    path('procesar-pedido/', views.process_order, name='process_order'),
    path('pedido-exitoso/<int:order_id>/', views.order_success, name='order_success'),
    path('order/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    # Asegúrate de tener también la URL para los detalles
    path('order/<int:order_id>/detail/', views.order_detail, name='order_detail'),

    
    ] 

   


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    


from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),

    # Dashboard principal
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
 
    # Gestión de usuarios
    path('admin-dashboard/users/', views.user_list, name='admin_user_list'),
    path('admin-dashboard/users/<int:user_id>/', views.user_detail, name='admin_user_detail'),
    path('admin-dashboard/users/<int:user_id>/toggle-status/', views.toggle_user_status, name='admin_toggle_user_status'),
    
    # Gestión de productos
    path('admin-dashboard/products/', views.product_list, name='admin_product_list'),
    path('admin-dashboard/products/new/', views.product_form, name='admin_product_new'),
    path('admin-dashboard/products/<int:product_id>/edit/', views.product_form, name='admin_product_edit'),
    path('admin-dashboard/products/<int:product_id>/toggle-availability/', views.toggle_product_availability, name='admin_toggle_product_availability'),
    path('admin/product/form/', views.product_form, name='admin_product_form'),
    path('admin/product/form/<int:product_id>/', views.product_form, name='admin_product_edit'),
    path('admin/product/image/<int:image_id>/', views.handle_product_image, name='admin_product_image_handle'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('product/image/<int:image_id>/delete/', views.delete_product_image, name='delete_product_image'),
    path('product/image/<int:image_id>/set-main/', views.set_main_image, name='set_main_image'),
    path('admin/product/form/', views.product_form, name='admin_product_form'),
    path('admin/product/form/<int:product_id>/', views.product_form, name='admin_product_edit'),
    path('admin/product/image/<int:image_id>/', views.handle_product_image, name='admin_product_image_handle'),

    # Gestión de categorías
    path('admin-dashboard/categories/', views.category_list, name='admin_category_list'),
    path('admin-dashboard/categories/new/', views.category_form, name='admin_category_new'),
    path('admin-dashboard/categories/<int:category_id>/edit/', views.category_form, name='admin_category_edit'),
    
    # Gestión de la empresa
    path('admin/associate-certification/<int:cert_id>/', views.associate_certification, name='admin_associate_certification'),

    path('admin-dashboard/company/', views.company_detail, name='admin_company_detail'),
    path('admin-dashboard/company/certifications/<int:certification_id>/delete/', views.delete_certification, name='admin_delete_certification'),
    path('admin-dashboard/company/add_employee/', views.add_employee, name='add_employee'),
    path('admin-dashboard/products/delete/<int:pk>/', views.product_delete, name='admin_product_delete'),
    path('admin-dashboard/categories/delete/<int:pk>/', views.category_delete, name='admin_category_delete'),
    path('categories/delete-all/', views.delete_all_categories, name='admin_category_delete_all'),
    path('admin/company/employee/<int:employee_id>/edit/', views.edit_employee, name='edit_employee'),
    path('admin/company/employee/<int:employee_id>/delete/', views.delete_employee, name='delete_employee'),
    
    # Reportes
    path('admin-dashboard/reports/sales/', views.sales_report, name='admin_sales_report'),
    path('admin/sales/<int:sale_id>/delete/', views.delete_sale, name='admin_delete_sale'),
    path('admin/sales/delete-selected/', views.delete_selected_sales, name='admin_delete_selected_sales'),
    path('admin/sales/delete-all/', views.delete_all_sales, name='admin_delete_all_sales'),
    
    
    
    path('admin-dashboard/reports/sales/excel/', views.sales_report_excel, name='admin_sales_report_excel'),
    path('admin-dashboard/reports/sales/pdf/', views.sales_report_pdf, name='admin_sales_report_pdf'),
    path('admin-dashboard/reset-database/', views.reset_database, name='admin_reset_database'),
    path('admin-dashboard/backup-database/', views.backup_database, name='admin_backup_database'),
    
    
    path('products/print-labels/', views.admin_print_product_labels, name='admin_print_product_labels'),
    
]

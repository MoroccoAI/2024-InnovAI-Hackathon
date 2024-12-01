from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('inventory/', views.inventory, name='inventory'),
    path('alerts/', views.alerts, name='alerts'),
    path('list-of-medicines/', views.list_of_medicines, name='list-of-medicines'),
    path('list-of-medicines/<int:page>/', views.list_of_medicines, name='list-of-medicines-paginated'),
    path('list-of-medicines/search/', views.list_of_medicines, name='list-of-medicines-search', kwargs={'q': ''}),
    path('sales-reports/', views.sales_reports, name='sales-reports'),
    path('stock-reports/', views.stock_reports, name='stock-reports'),
    path('predictions/', views.predictions, name='predictions'),
    path('drug-details/', views.drug_details, name='drug-details'),
    path('add-medicine/', views.add_medicine, name='add-medicine'),
    path('settings/', views.settings, name='settings'),
    path('stock-history/', views.stock_history, name='stock-history'),
    path('loading/', views.loading, name='loading'),
    
    # new ones by fayz
    path('edit-medicine/<int:drug_id>/', views.edit_medicine, name='edit-medicine'),
    path('delete-medicine/<int:drug_id>/', views.delete_medicine, name='delete-medicine'),
    path('medicine-groups/', views.medicine_groups, name='medicine-groups'),
    path('drug-details/<int:drug_id>/', views.drug_details, name='drug-details'),
    
    path('generate-sales-report/', views.generate_sales_report, name='generate-sales-report'),
    path('generate-stock-report/', views.generate_stock_report, name='generate-stock-report'),

    path('assistant/', views.assistant, name='assistant'),

    path('list-of-sales/', views.list_of_sales, name='list-of-sales'),
    path('list-of-sales/<int:page>/', views.list_of_sales, name='list-of-sales-paginated'),
    path('add-sale/', views.add_sale, name='add-sale'),
    path('sale-details/<int:sale_id>/', views.sale_details, name='sale-details'),
    
]
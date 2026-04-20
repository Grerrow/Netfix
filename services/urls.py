from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_of_services, name='services_list'),
    path('create/', views.create_service, name='create_service'),
    path('<int:id>', views.single_service, name='single_service'),
    path('<int:id>/request_service/', views.request_service, name='request_service'),
    path('<slug:field>/', views.services_per_field, name='services_field'),
]

from django.urls import path
from django.contrib.auth import views

from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("company/", views.CompanySignUpView.as_view(), name="register_company"),
    path("customer/", views.CustomerSignUpView.as_view(), name="register_customer"),
    # as_view() is a method provided by Django that creates an instance of the class-based view (CustomerSignUpView)
    # and makes it callable as a normal view function
]

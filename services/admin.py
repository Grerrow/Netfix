from django.contrib import admin
from .models import Service, RequestService


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "price_hour", "field", "date")


@admin.register(RequestService)
class RequestServiceAdmin(admin.ModelAdmin):
    list_display = ("service", "customer", "company", "calculated_cost", "requested_date", "service_hours")

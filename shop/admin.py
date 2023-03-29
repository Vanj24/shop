from django.contrib import admin
from .models import Customer, Brand, Product, Invoice

admin.site.register(Customer)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Invoice)

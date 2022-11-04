from django.contrib import admin
from .models import Product,ShippingAdress,Order,OrderItem,Review

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAdress)
admin.site.register(Review)
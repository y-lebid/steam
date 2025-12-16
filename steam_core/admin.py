from django.contrib import admin
from .models import Product, CartItem, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'session_key', 'created_at')
    search_fields = ('session_key', 'product__name')



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'email', 'created_at', 'is_processed')
    list_filter = ('is_processed',)

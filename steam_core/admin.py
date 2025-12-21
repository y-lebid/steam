from django.contrib import admin
from .models import Product, CartItem, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_available")
    search_fields = ("name",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "email", "created_at", "is_processed")
    list_filter = ("is_processed", "created_at")
    search_fields = ("phone", "email")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")

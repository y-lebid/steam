from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    min_requirements = models.TextField(
        blank=True,
        verbose_name="Мінімальні системні вимоги"
    )
    rec_requirements = models.TextField(
        blank=True,
        verbose_name="Рекомендовані системні вимоги"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=40)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    session_key = models.CharField(max_length=40)

    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
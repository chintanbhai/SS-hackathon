from django.db import models

# Consumer model
class Consumer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Order model
class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('one_time', 'One-Time'),
        ('subscription', 'Subscription'),
    ]
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='one_time')
    order_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # For subscriptions

    def __str__(self):
        return f"{self.consumer.name} - {self.product.name} ({self.order_type})"

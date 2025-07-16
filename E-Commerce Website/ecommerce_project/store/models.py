from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)  # discounted price
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=100.0)  # original MRP
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name

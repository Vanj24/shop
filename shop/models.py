from django.db import models
from django.utils import timezone
from .enums import CurrencyEnum, StatusEnum
import uuid


class Customer(models.Model):
    customer_number = models.CharField(max_length=16, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_terminated = models.BooleanField(default=False)
    added_by = models.ForeignKey('auth.User', related_name='customer_added_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey('auth.User', related_name='customer_updated_by', on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def status(self):
        return StatusEnum.ACTIVE.value if self.is_active else StatusEnum.TERMINATED.value

    def change_status(self):
        self.is_active = not self.is_active
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.customer_number = f"CUSTOMER{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)


class Brand(models.Model):
    brand_name = models.CharField(max_length=255)
    brand_code = models.CharField(max_length=16)
    logo = models.ImageField(upload_to='logos/')

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_number = models.CharField(max_length=16, unique=True)
    currency = models.CharField(max_length=3, choices=[(tag.name, tag.value) for tag in CurrencyEnum])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    next_billing_date = models.DateTimeField()
    previous_billing_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_terminated = models.BooleanField(default=False)
    added_by = models.ForeignKey('auth.User', related_name='product_added_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey('auth.User', related_name='product_updated_by', on_delete=models.CASCADE)

    def status(self):
        return StatusEnum.ACTIVE.value if self.is_active else StatusEnum.TERMINATED.value

    def change_status(self):
        self.is_active = not self.is_active
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.product_number = f"PRODUCT{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_number


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=16, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.invoice_number = f"INVOICE{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number

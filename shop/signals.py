from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Product, Customer, Invoice


@receiver(pre_save, sender=Product)
def set_product_number(sender, instance, **kwargs):
    if not instance.product_number:
        instance.product_number = 'PRODUCT' + str(instance.id).zfill(4)


@receiver(pre_save, sender=Customer)
def set_customer_number(sender, instance, **kwargs):
    if not instance.customer_number:
        instance.customer_number = 'CUSTOMER' + str(instance.id).zfill(4)


@receiver(pre_save, sender=Invoice)
def set_invoice_number(sender, instance, **kwargs):
    if not instance.invoice_number:
        instance.invoice_number = 'INVOICE' + str(instance.id).zfill(4)

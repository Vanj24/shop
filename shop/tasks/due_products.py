from datetime import timedelta
from django.utils import timezone
from shop.models import Product, Invoice


def get_due_products(brand):
    due_products = []
    now = timezone.now()
    print(f"Today: {now.date()}")
    print(f"Processing products for brand {brand.brand_name}:")
    for product in Product.objects.filter(brand=brand, is_active=True):
        print(f"Product {product.pk}: next_billing_date={product.next_billing_date}")
        if product.next_billing_date.date() <= now.date():
            due_products.append(product)
            print(f"  -> Due product: {product.pk}")
    return due_products


def create_invoice_for_product(due_products):
    invoices_created = []

    for product in due_products:
        invoice = Invoice.objects.create(
            invoice_number=f"INVOICE{Invoice.objects.count() + 1:04d}",
            customer=product.customer,
            description=f"Invoice for {product.description}",
            product=product,
            total_price=product.price,
        )
        invoices_created.append(invoice)

        print(f"Invoice created: {invoice}")
        print(f"Old next_billing_date: {product.next_billing_date}")
        print(f"Old previous_billing_date: {product.previous_billing_date}")

        product.previous_billing_date = timezone.now()
        product.next_billing_date = timezone.now() + timedelta(days=30)
        product.save()

        print(f"New next_billing_date: {product.next_billing_date}")
        print(f"New previous_billing_date: {product.previous_billing_date}")
        print("---")

    return invoices_created

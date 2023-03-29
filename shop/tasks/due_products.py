from django.utils import timezone
from shop.models import Customer, Product, Invoice


def get_due_products(brand):
    today = timezone.now().date()
    due_products = Product.objects.filter(
        brand=brand,
        customer__is_terminated=False,
        next_billing_date__lte=today
    )
    return due_products


def create_invoice_for_product(due_products):
    invoices_created = []
    for product in due_products:
        invoice = Invoice.objects.create(
            customer=product.customer,
            description=f"Invoice for {product.product_number}",
            product=product,
            total_price=product.price
        )
        if invoice:
            product.previous_billing_date = invoice.created_at
            product.next_billing_date = invoice.created_at + timezone.timedelta(days=30)
            product.save()
            invoices_created.append(invoice)

    return invoices_created

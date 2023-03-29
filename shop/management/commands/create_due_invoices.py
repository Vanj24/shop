from django.core.management.base import BaseCommand
from shop.models import Brand
from shop.tasks.due_products import get_due_products, create_invoice_for_product


class Command(BaseCommand):
    help = 'Create invoices for due products'

    def handle(self, *args, **options):
        for brand in Brand.objects.all():
            due_products = get_due_products(brand)
            invoices_created = create_invoice_for_product(due_products)
            self.stdout.write(self.style.SUCCESS(
                f'Created {len(invoices_created)} invoices for brand {brand.brand_name}'))

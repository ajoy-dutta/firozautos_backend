from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from transaction.models import PurchaseEntry
from decimal import Decimal



@receiver(post_save, sender = PurchaseProduct)
def update_stock_product(sender, instance, created, **kwargs):

    if not created:
        return
    

    company_name = instance.purchase.company_name
    part_no = instance.part_no
    product = instance.product

    

    stock, created_stock = StockProduct.objects.get_or_create(
        company_name = company_name,
        part_no = part_no,
        defaults={
            'product': product,
            'purchase_quantity': instance.purchase_quantity,
            'current_stock_quantity': instance.purchase_quantity,
            'purchase_price': instance.purchase_price,
            'sale_price': instance.purchase_price_with_percentage,
            'current_stock_value': instance.purchase_price * instance.purchase_quantity
        }
    )


    if not created_stock:
        pq = int(instance.purchase_quantity)
        pp = Decimal(instance.purchase_price)
        ppwp = Decimal(instance.purchase_price_with_percentage)

        stock.purchase_quantity += pq
        stock.current_stock_quantity += pq
        stock.purchase_price = pp
        stock.sale_price = ppwp
        stock.current_stock_value += pp * pq
        stock.save()






@receiver(post_save, sender=PurchaseEntry)
def update_stock_on_purchase(sender, instance, created, **kwargs):
    if created:
        company_name = instance.company_name
        part_no = instance.part_no
        quantity = int(instance.quantity)
        purchase_price = Decimal(instance.purchase_price)

        try:
            product = Product.objects.get(company__company_name=company_name, part_no=part_no)
        except Product.DoesNotExist:
            return

        # get or create StockProduct
        stock, _ = StockProduct.objects.get_or_create(
            company_name=company_name,
            part_no=part_no,
            product=product,
            defaults={
                'purchase_quantity': 0,
                'sale_quantity': 0,
                'damage_quantity': 0,
                'current_stock_quantity': 0,
                'purchase_price': purchase_price,
                'sale_price': 0,
                'current_stock_value': 0,
            }
        )

        # update quantities
        stock.purchase_quantity += quantity
        stock.current_stock_quantity += quantity

        # update pricing if needed
        stock.purchase_price = purchase_price
        stock.current_stock_value = stock.current_stock_quantity * stock.purchase_price

        stock.save()
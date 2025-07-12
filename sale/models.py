from django.db import models
from person.models import Customer
from product.models import Product
from master.models import Company
from django.utils import timezone

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    sale_date = models.DateField(default=timezone.now)
    invoice_no = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_payable_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_invoice_no(self):
        last_id = Sale.objects.all().order_by('-id').first()
        next_number = (last_id.id + 1) if last_id else 1
        return f'SA{next_number:08d}'

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            self.invoice_no = self.generate_invoice_no()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_no} - {self.customer.customer_name}"



class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    part_no = models.CharField(max_length=100)
    sale_quantity = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    sale_price_with_percentage = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    returned_quantity = models.PositiveIntegerField(default=0)  # New field for tracking returns

    def __str__(self):
        return f"{self.product.part_no} ({self.sale.invoice_no})"


class SaleReturn(models.Model):
    sale_product = models.ForeignKey(SaleProduct, related_name='returns', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    return_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Return {self.quantity} of {self.sale_product} on {self.return_date}"

class SalePayment(models.Model):
    sale = models.ForeignKey(Sale, related_name='payments', on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=100, blank=True, null=True)
    cheque_no = models.CharField(max_length=100, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment for {self.sale.invoice_no}"

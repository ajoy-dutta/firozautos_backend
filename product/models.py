from django.db import models
from django.utils import timezone
from person.models import Supplier
from master.models import Company



class ProductCategory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product_categories')
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.company.company_name} - {self.category_name}"



class Product(models.Model):
    company = models.ForeignKey("master.Company", on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey("ProductCategory", on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)  
    part_no = models.CharField(max_length=100)
    product_code = models.CharField(max_length=100, blank=True, null=True)
    hs_code = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    brand_name = models.CharField(max_length=100, blank=True, null=True) 
    model_no = models.CharField(max_length=100, blank=True, null=True) 
    net_weight = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    remarks = models.CharField(max_length=100, blank=True, null=True) 
    product_mrp = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    percentage = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    product_bdt = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    remarks = models.TextField(blank=True,null=True)
    
    def save(self, *args, **kwargs):
        if not self.product_code:
            last_product = Product.objects.order_by('-id').first()
            if last_product and last_product.product_code and last_product.product_code.startswith("PROD"):
                last_number = int(last_product.product_code.replace("PROD", ""))
            else:
                last_number = 0
            self.product_code = f"PROD{last_number + 1:03d}"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.company.company_name} - {self.category.category_name} - {self.product_name}"
    




class SupplierPurchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    purchase_date = models.DateField()
    invoice_no = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_payable_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice_no} - {self.supplier.supplier_name}"




class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(SupplierPurchase, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    part_no = models.CharField(max_length=100)
    purchase_quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    purchase_price_with_percentage = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.part_no} ({self.purchase.invoice_no})"




class PurchasePayment(models.Model):
    purchase = models.ForeignKey(SupplierPurchase, related_name='payments', on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=100, blank=True, null=True)
    cheque_no = models.CharField(max_length=100, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Payment for {self.purchase.invoice_no}"

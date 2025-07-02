from django.db import models
from django.utils import timezone

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    incharge_name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name
    

class ProductCategory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product_categories')
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.company.company_name} - {self.category_name}"


class Product(models.Model):
    company = models.ForeignKey("Company", on_delete=models.CASCADE, related_name='products')
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
    

class CostCategory(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class SourceCategory(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name

class PaymentMode(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class DistrictMaster(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CountryMaster(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SupplierTypeMaster(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BankCategoryMaster(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BankMaster(models.Model):
    name = models.CharField(max_length=100)
    bank_category = models.ForeignKey(BankCategoryMaster, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

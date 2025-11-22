from django.db import models
from django.utils import timezone
from person.models import Supplier
from master.models import Company
from django.utils.timezone import now
from django.utils.text import slugify


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
    bike_model = models.ForeignKey("product.BikeModel", on_delete=models.SET_NULL, blank=True,null=True,related_name="products") 
    net_weight = models.DecimalField(max_digits=12, decimal_places=3, default=0)
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
    


class BikeModel(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="bike_models")
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to="bike_models/", blank=True, null=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)

    class Meta:
        unique_together = ("company", "name")
        ordering = ["company__company_name", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.company_id}-{self.name}")[:160]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company.company_name} - {self.name}"





class StockProduct(models.Model):
    company_name = models.CharField(max_length=255)
    part_no = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    purchase_quantity = models.PositiveIntegerField(default=0)
    sale_quantity = models.PositiveIntegerField(default=0)
    damage_quantity = models.PositiveIntegerField(default=0)
    current_stock_quantity = models.PositiveIntegerField(default=0)

    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_stock_value = models.DecimalField(max_digits=14, decimal_places=2)

    net_weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    damage_product = models.TextField(blank=True, null=True)
    product_sale_summary = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.part_no}"


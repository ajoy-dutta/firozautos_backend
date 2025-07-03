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

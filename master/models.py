from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    incharge_name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

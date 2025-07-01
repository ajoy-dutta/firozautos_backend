from django.db import models



class Loan(models.Model):

    date = models.DateField()
    source_category = models.CharField(max_length=100)
    bank_category = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    loan_type = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=50, blank=True, null=True )
    principal_amount = models.DecimalField(max_digits=15, decimal_places=2)
    rate_percent = models.DecimalField(max_digits=5, decimal_places=2)
    number_of_months = models.PositiveIntegerField()
    interest_amount = models.DecimalField(max_digits=15, decimal_places=2)
    total_payable_amount = models.DecimalField(max_digits=15, decimal_places=2)
    installment_per_month = models.DecimalField(max_digits=15, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank_name or 'Loan'} - {self.date}"
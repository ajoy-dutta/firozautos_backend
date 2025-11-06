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
    




class PurchaseEntry(models.Model):
    invoice_no = models.CharField(max_length=100, default='AUTO GENERATE')
    purchase_date = models.DateField()
    exporter_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    part_no = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice: {self.invoice_no} on {self.purchase_date}"
    



class Expense(models.Model):
    TRANSACTION_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('cheque', 'Cheque'),
        ('bkash', 'Bkash'),
    ]

    date = models.DateField()
    voucherNo = models.CharField(max_length=30, unique=True)
    accountTitle = models.CharField(max_length=100)
    costCategory = models.CharField(max_length=100)
    employeeName = models.CharField(max_length=100, blank=True, null=True)
    borrowerName = models.CharField(max_length=100, blank=True, null=True)
    owedName = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Transaction-related
    transactionType = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    bankName = models.CharField(max_length=100, blank=True, null=True)
    accountNo = models.CharField(max_length=50, blank=True, null=True)
    chequeNo = models.CharField(max_length=50, blank=True, null=True)
    bkashNumber = models.CharField(max_length=20, blank=True, null=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voucherNo} - {self.accountTitle} - {self.amount}"





class Income(models.Model):
    TRANSACTION_TYPES = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
    ]

    COST_CATEGORIES = [
        ('salary', 'Salary Statement'),
        ('sale_return', 'Sale Return'),
        ('borrow_pay', 'Borrow Pay'),
        ('owed_return', 'Owed Return'),
    ]

    date = models.DateField()
    voucherNo = models.CharField(max_length=100)
    accountTitle = models.CharField(max_length=200)
    sourceCategory = models.CharField(max_length=50, choices=COST_CATEGORIES)
    employeeName = models.CharField(max_length=100, blank=True, null=True)
    borrowerName = models.CharField(max_length=100, blank=True, null=True)
    owedName = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    bankName = models.CharField(max_length=100, blank=True, null=True)
    accountNo = models.CharField(max_length=50, blank=True, null=True)
    chequeNo = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transactionType = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voucherNo} - {self.accountTitle} - {self.amount}"

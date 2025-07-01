from django.db import models
from rest_framework.permissions import BasePermission
from master.models import*

class IsStaffOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)

class Exporter(models.Model):
    company_name = models.CharField(max_length=255)
    exporter_name = models.CharField(max_length=255)
    mail_address = models.EmailField()
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.exporter_name}"
    

class Employee(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    RELIGION_CHOICES = [('Islam', 'Islam'), ('Hinduism', 'Hinduism'), ('Christianity', 'Christianity'), ('Other', 'Other')]

    employee_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    employee_code = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES,blank=True,null=True)
    birth_id_no = models.CharField(max_length=100, blank=True, null=True)
    nid_no = models.CharField(max_length=100, blank=True, null=True)
    passport_no = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=50, default="Bangladeshi")
    email = models.EmailField(blank=True, null=True)
    mobile_no = models.CharField(max_length=20,blank=True, null=True)
    father_mobile_no = models.CharField(max_length=20, blank=True, null=True)
    mother_mobile_no = models.CharField(max_length=20, blank=True, null=True)
    other_mobile_no = models.CharField(max_length=20, blank=True, null=True)
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Address
    country = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    division = models.CharField(max_length=100, blank=True, null=True)
    police_station = models.CharField(max_length=100, blank=True, null=True)
    post_office = models.CharField(max_length=100, blank=True, null=True)
    town_or_village = models.CharField(max_length=100, blank=True, null=True)

    # Experience
    previous_work = models.CharField(max_length=255, blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    shop_address = models.TextField(blank=True, null=True)

    # Bank Account
    account_name = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    branch_address = models.CharField(max_length=255, blank=True, null=True)

    # Mobile Banking
    bkash_no = models.CharField(max_length=20, blank=True, null=True)
    roket_no = models.CharField(max_length=20, blank=True, null=True)
    nagad_no = models.CharField(max_length=20, blank=True, null=True)

    # Reference
    reference_by = models.CharField(max_length=255, blank=True, null=True)
    reference_mobile = models.CharField(max_length=20, blank=True, null=True)
    reference_address = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.employee_code:
            last_employee = Employee.objects.order_by('-id').first()
            last_number = 0
            if last_employee and last_employee.employee_code and last_employee.employee_code.startswith("FA"):
                try:
                    last_number = int(last_employee.employee_code.replace("FA", ""))
                except:
                    pass
            self.employee_code = f"FA{last_number + 1:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.employee_name

class Education(models.Model):
    employee = models.ForeignKey(Employee, related_name='education', on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=255)
    institute_name = models.CharField(max_length=255)
    passing_year = models.CharField(max_length=10)
    group_or_subject = models.CharField(max_length=100)
    gpa_or_dvision = models.CharField(max_length=50)
    board_or_university = models.CharField(max_length=100)





class Supplier(models.Model):
    supplier_name = models.CharField(max_length=200)
    district = models.ForeignKey(DistrictMaster, on_delete=models.PROTECT)
    country = models.CharField(max_length=100)
    supplier_type = models.ForeignKey(SupplierTypeMaster, on_delete=models.PROTECT)
    shop_name = models.CharField(max_length=200, blank=True, null=True)
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    nid_no = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    previous_due_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.supplier_name




class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    district = models.CharField(max_length=100, blank=True, null=True)
    customer_type = models.CharField(max_length=100, blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    nid_no = models.CharField(max_length=100, blank=True, null=True)
    courier_name = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    previous_due_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

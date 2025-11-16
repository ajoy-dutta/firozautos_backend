from rest_framework import viewsets
from .models import*
from .serializers import*
from .permissions import IsStaffOrAdmin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
import calendar
import datetime

class ExporterViewSet(viewsets.ModelViewSet):
    queryset = Exporter.objects.all()
    serializer_class = ExporterSerializer
    permission_classes = [IsStaffOrAdmin]



class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        education_raw = self.request.data.get('education', '[]')
        try:
            education = json.loads(education_raw)
        except json.JSONDecodeError:
            education = []

        serializer.save(education=education)

    def perform_update(self, serializer):
        education_raw = self.request.data.get('education', '[]')
        try:
            education = json.loads(education_raw)
        except json.JSONDecodeError:
            education = []

        serializer.save(education=education)

class EmployeeAttendanceViewSet(viewsets.ModelViewSet):
    queryset = EmployeeAttendance.objects.all().order_by("-date")
    serializer_class = EmployeeAttendanceSerializer
    permission_classes = [IsStaffOrAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        employee_id = self.request.query_params.get("employee_id")
        from_date = self.request.query_params.get("from_date")
        to_date = self.request.query_params.get("to_date")

        if employee_id:
            qs = qs.filter(employee_id=employee_id)
        if from_date and to_date:
            qs = qs.filter(date__range=[from_date, to_date])

        return qs
    
class EmployeeSalaryTransactionViewSet(viewsets.ModelViewSet):
    queryset = EmployeeSalaryTransaction.objects.all()
    serializer_class = EmployeeSalaryTransactionSerializer
    permission_classes = [IsStaffOrAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        employee_id = self.request.query_params.get("employee_id")
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")

        if employee_id:
            qs = qs.filter(employee_id=employee_id)
        if year:
            qs = qs.filter(year=year)
        if month:
            qs = qs.filter(month=month)

        return qs
    
class EmployeeSalarySummary(APIView):
    permission_classes = [IsStaffOrAdmin]

    def get(self, request, *args, **kwargs):
        employee_id = request.query_params.get("employee_id")
        year = request.query_params.get("year")
        month = request.query_params.get("month")

        if not (employee_id and year and month):
            return Response(
                {"detail": "employee_id, year, and month are required."},
                status=400
            )

        year = int(year)
        month = int(month)

        try:
            employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=404)

        base_salary = employee.salary_amount or 0

        # 🔹 Total calendar days in month (1–30/31)
        total_days_in_month = calendar.monthrange(year, month)[1]

        # 🔹 Count working days (exclude Fridays)
        working_days = 0
        for day in range(1, total_days_in_month + 1):
            date_obj = datetime.date(year, month, day)
            # weekday(): 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
            if date_obj.weekday() != 4:  # Skip Friday
                working_days += 1

        # 🔹 Attendance counts
        present_days = EmployeeAttendance.objects.filter(
            employee=employee,
            date__year=year,
            date__month=month,
            status="present",
        ).count()

        absent_days_marked = EmployeeAttendance.objects.filter(
            employee=employee,
            date__year=year,
            date__month=month,
            status="absent",
        ).count()

        # 🔹 Decide how to count absents
        if absent_days_marked > 0:
            # If you explicitly marked absents, trust that
            absent_days = absent_days_marked
        else:
            # Otherwise, assume missing working days are absent
            absent_days = working_days - present_days

        if absent_days < 0:
            absent_days = 0

        # 🔹 Per-day salary based on working days
        per_day_salary = base_salary / working_days if working_days else 0
        salary_cut = per_day_salary * absent_days
        net_salary = base_salary - salary_cut

        # 🔹 Salary Transactions
        advance_paid = EmployeeSalaryTransaction.objects.filter(
            employee=employee,
            year=year,
            month=month,
            transaction_type="advance"
        ).aggregate(total=Sum("amount"))["total"] or 0

        salary_paid = EmployeeSalaryTransaction.objects.filter(
            employee=employee,
            year=year,
            month=month,
            transaction_type="salary"
        ).aggregate(total=Sum("amount"))["total"] or 0

        total_paid = advance_paid + salary_paid
        remaining_salary = net_salary - total_paid

        data = {
            "employee_id": employee.id,
            "employee_name": employee.employee_name,
            "employee_code": employee.employee_code,
            "year": year,
            "month": month,
            "base_salary": base_salary,
            "total_days_in_month": total_days_in_month,  # calendar days
            "total_working_days": working_days,          # excluding Fridays
            "present_days": present_days,
            "absent_days": absent_days,                  # ✅ now respects marked absents
            "per_day_salary": per_day_salary,
            "salary_cut": salary_cut,
            "net_salary": net_salary,
            "advance_paid": advance_paid,
            "salary_paid": salary_paid,
            "total_paid": total_paid,
            "remaining_salary": remaining_salary,
        }

        return Response(data)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('-created_at')
    serializer_class = SupplierSerializer



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [IsStaffOrAdmin]


class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all().order_by('-created_at')
    serializer_class = BorrowerSerializer
    permission_classes = [IsStaffOrAdmin]


class OweViewSet(viewsets.ModelViewSet): 
    queryset = Owed.objects.all().order_by('-created_at')
    serializer_class = OweSerializer
    permission_classes = [IsStaffOrAdmin]
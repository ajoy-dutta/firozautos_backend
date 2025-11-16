from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

router = DefaultRouter()

router.register(r'exporters', ExporterViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'borrowers', BorrowerViewSet)
router.register(r'owe', OweViewSet)
router.register(r'employee-attendance', EmployeeAttendanceViewSet)
router.register(r'employee-salary-transactions', EmployeeSalaryTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('employee-salary-summary/', EmployeeSalarySummary.as_view(), name='employee-salary-summary'),
]

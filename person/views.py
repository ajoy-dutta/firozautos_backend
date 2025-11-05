from rest_framework import viewsets
from .models import*
from .serializers import*
from .permissions import IsStaffOrAdmin


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
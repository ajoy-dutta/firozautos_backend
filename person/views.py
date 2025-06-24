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
    permission_classes = [IsStaffOrAdmin]



from django.shortcuts import render
from rest_framework import viewsets
from .models import Sale
from .serializers import SaleSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-sale_date')
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

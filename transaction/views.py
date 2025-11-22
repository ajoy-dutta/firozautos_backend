from rest_framework import generics, viewsets
from .models import *
from master.models import Company
from django.db import transaction
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.dateparse import parse_date



class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all().order_by('-date')
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]





class ExpenseViewset(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]




class IncomeViewset(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSrializer
    permission_classes = [IsAuthenticatedOrReadOnly]


from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly




class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all().order_by('-date')
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]




class PurchaseEntryListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseEntry.objects.all().order_by('-purchase_date')
    serializer_class = PurchaseEntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PurchaseEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseEntry.objects.all()
    serializer_class = PurchaseEntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

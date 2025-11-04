from rest_framework import generics, viewsets
from .models import *
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




class PurchaseEntryListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseEntry.objects.all().order_by('-purchase_date')
    serializer_class = PurchaseEntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PurchaseEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseEntry.objects.all()
    serializer_class = PurchaseEntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]




class ExpenseViewset(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params

        from_date = params.get('fromDate')
        to_date = params.get('toDate')
        receipt_no = params.get('receiptNo')
        account_title = params.get('accountTitle')
        cost_category = params.get('costCategory')

        # ✅ Date filtering (parse and check validity)
        if from_date and to_date:
            from_date = parse_date(from_date)
            to_date = parse_date(to_date)
            if from_date and to_date:
                queryset = queryset.filter(date__range=[from_date, to_date])

        # ✅ Other filters
        if receipt_no:
            queryset = queryset.filter(voucherNo__icontains=receipt_no)
        if account_title:
            queryset = queryset.filter(accountTitle__icontains=account_title)
        if cost_category and cost_category.lower() != 'all':
            queryset = queryset.filter(costCategory=cost_category)

        return queryset



class IncomeViewset(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSrializer
    permission_classes = [IsAuthenticatedOrReadOnly]

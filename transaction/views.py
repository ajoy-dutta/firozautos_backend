from rest_framework import generics, viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import SupplierPurchase
from .serializers import CombinedPurchaseSerializer




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




class CombinedPurchaseView(APIView):
    def get(self, request):

        company = request.query_params.get("company")
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        purchases = SupplierPurchase.objects.prefetch_related("products__product", "supplier").all()
        grouped_data = []


        if company:
            purchases = purchases.filter(company_name__iexact=company)
        if from_date:
            purchases = purchases.filter(purchase_date__gte=parse_date(from_date))
        if to_date:
            purchases = purchases.filter(purchase_date__lte=parse_date(to_date))


        for purchase in purchases:
            # All product names and part numbers
            product_names = []
            part_no_list = []
            total_qty = 0
            total_amt = 0

            for item in purchase.products.all():
                if item.product:
                    name_part = f"{item.product.product_name}"
                    product_names.append(name_part)
                else:
                    product_names.append("—")
                
                if item.product:
                    part_no = f"{item.product.part_no}"
                    part_no_list.append(part_no)
                else:
                    part_no_list.append("—")

                total_qty += item.purchase_quantity
                total_amt += float(item.total_price)

            grouped_data.append({
                "date": purchase.purchase_date,
                "invoice_no": purchase.invoice_no,
                "part_no" : "|".join(part_no_list),
                "product_name": "|".join(product_names),
                "supplier_or_exporter":  purchase.supplier.supplier_name,
                "quantity": total_qty,
                "purchase_amount": round(total_amt, 2),
            })


        purchase_entries = PurchaseEntry.objects.all()

        if company:
            purchase_entries = purchase_entries.filter(company_name__iexact=company)
        if from_date:
            purchase_entries = purchase_entries.filter(purchase_date__gte=parse_date(from_date))
        if to_date:
            purchase_entries = purchase_entries.filter(purchase_date__lte=parse_date(to_date))

        for pe in purchase_entries:
            grouped_data.append({
                "date": pe.purchase_date,
                "invoice_no": pe.invoice_no,
                "part_no": pe.part_no,
                "product_name": "",  # No FK to Product
                "supplier_or_exporter": pe.exporter_name,
                "quantity": pe.quantity,
                "purchase_amount": pe.total_price,
            })

        print("Grouped Data", grouped_data)

        # --- Sort by Date Descending ---
        grouped_data.sort(key=lambda x: x["date"], reverse=True)

        serializer = CombinedPurchaseSerializer(grouped_data, many=True)
        return Response(serializer.data)


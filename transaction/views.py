from rest_framework import generics, viewsets
from .models import *
from product.models import Product, StockProduct
from master.models import Company
import pandas as pd
from django.db import transaction
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import SupplierPurchase, PurchaseProduct
from .serializers import CombinedPurchaseSerializer
from decimal import Decimal
from django.db.models import Prefetch





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

        company_name = request.query_params.get("company")
        part_no = request.query_params.get("part_no")
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")
        grouped_data = []


        supplier_purchases = (
            SupplierPurchase.objects
            .select_related("supplier")          # forward FK → best option
            .prefetch_related("products__product")  # reverse FK + nested FK
        )

        if company_name:
            supplier_purchases = supplier_purchases.filter(company_name__iexact=company_name)
        if from_date:
            supplier_purchases = supplier_purchases.filter(purchase_date__gte=parse_date(from_date))
        if to_date:
            supplier_purchases = supplier_purchases.filter(purchase_date__lte=parse_date(to_date))

        for purchase in supplier_purchases:

            # All product names and part numbers
            product_names = []
            part_no_list = []
            total_qty = 0
            total_amt = 0

            for item in purchase.products.all():
                # for Part Wise Filtering
                if part_no:
                    if item.product and item.product.part_no != part_no:
                        continue

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

            if total_qty == 0:
                continue

            grouped_data.append({
                "date": purchase.purchase_date,
                "invoice_no": purchase.invoice_no,
                "part_no" : "|".join(part_no_list),
                "product_name": "|".join(product_names),
                "supplier_or_exporter":  purchase.supplier.supplier_name,
                "quantity": total_qty,
                "purchase_amount": round(total_amt, 2),
            })

            print("Grouped Data", grouped_data)



        # Purchase from Exporter
        purchases = Purchase.objects.prefetch_related('items__product').all()

        if company_name:
            purchases = purchases.filter(company_name__iexact=company_name)
        if from_date:
            purchases = purchases.filter(purchase_date__gte=parse_date(from_date))
        if to_date:
            purchases = purchases.filter(purchase_date__lte=parse_date(to_date))

        for purchase in purchases:
            product_names = []
            part_no_list = []
            total_qty = 0
            total_amt = 0


            for item in purchase.items.all():
                # for Part Wise Filtering
                if part_no:
                    if item.product and item.product.part_no != part_no:
                        continue

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

                total_qty += item.quantity
                total_amt += float(item.total_price)


            if total_qty == 0:
                continue
        
            grouped_data.append({
                "date": purchase.purchase_date,
                "invoice_no": purchase.invoice_no,
                "part_no": part_no_list,
                "product_name": product_names,  
                "supplier_or_exporter": purchase.exporter_name,
                "quantity": total_qty,
                "purchase_amount": total_amt,
            })

        # print("Grouped Data", grouped_data)

        # --- Sort by Date Descending ---
        grouped_data.sort(key=lambda x: x["date"], reverse=True)

        serializer = CombinedPurchaseSerializer(grouped_data, many=True)
        return Response(serializer.data)






def create_purchase_entry(data):
    try:
        company = Company.objects.get(id=data["company_id"])
    except Company.DoesNotExist:
        raise ValueError("Company not found")
    

    try:
        product = Product.objects.get(part_no=data["part_no"])
    except Product.DoesNotExist:
        raise ValueError("Product not found")

    # Get or create the Purchase
    purchase, created = Purchase.objects.get_or_create(
        invoice_no=data["invoice_no"],
        purchase_date =data["purchase_date"],
        defaults={
            "exporter_name": data["exporter_name"],
            "company_name": company.company_name,
        }
    )

    # Create PurchaseItem
    purchase_item = PurchaseItem.objects.create(
        purchase=purchase,
        product=product,
        quantity=data["quantity"],
        purchase_price=data["purchase_price"],
        total_price= Decimal(data["quantity"]) * Decimal(data["purchase_price"]),
    )

    return purchase_item




def update_stock(product, company_name, quantity, price, unit):
    
    stock, created = StockProduct.objects.get_or_create(
        product=product,
        part_no=product.part_no,
        defaults={
            "company_name": company_name,
            "purchase_quantity": quantity,
            "sale_quantity": 0,
            "damage_quantity": 0,
            "current_stock_quantity": quantity,
            "purchase_price": price,
            "sale_price": price,
            "current_stock_value": quantity * price,
        }
    )

    

    if not created:
        stock.purchase_quantity += quantity
        stock.current_stock_quantity += quantity
        stock.purchase_price = price
        stock.current_stock_value += Decimal(quantity) * Decimal(price)
        stock.save()

    return stock


class UploadStockExcelView(APIView):
    def post(self, request):
        file = request.FILES.get("xl_file")
        company_id = request.data.get("company_name")
        exporter_name = request.data.get("exporter_name")
        invoice_no = request.data.get("invoice_no", "AUTO_GENERATE")
        purchase_date = request.data.get("purchase_date")

        # Validate company
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "No Company Selected or Found"}, status=400)

        # Validate file
        if not file:
            return Response({"error": "No file uploaded"}, status=400)
        if not file.name.endswith(".xlsx"):
            return Response({"error": "Please upload an .xlsx file"}, status=400)

        # Read Excel
        try:
            df = pd.read_excel(file, engine="openpyxl")
        except Exception as e:
            return Response({"error": f"Invalid Excel file: {str(e)}"}, status=400)

        
        created_stocks = []
        with transaction.atomic():
            for _, row in df.iterrows():
                part_no = str(row["Part_no"]).strip()
                price = float(row["Rate"])
                quantity = int(row["Qty"])
                unit = str(row["Unit"])

                try:
                    product = Product.objects.get(part_no=part_no)
                except Product.DoesNotExist:
                    continue

                # Update product MRP
                product.product_mrp = price
                product.save()

                # Update stock using the helper function
                update_stock(product, company.company_name, quantity, price, unit)

                # Create purchase entry
                create_purchase_entry({
                    "invoice_no": invoice_no,
                    "purchase_date": purchase_date,
                    "exporter_name": exporter_name,
                    "company_id": company_id,
                    "part_no": part_no,
                    "quantity": quantity,
                    "purchase_price": price,
                })

                created_stocks.append({
                    "product": product.product_name,
                    "part_no": product.part_no,
                    "added_quantity": quantity,
                    "updated_mrp": price,
                })

        return Response({
            "message": "Stock uploaded successfully",
            "items": created_stocks
        }, status=200)
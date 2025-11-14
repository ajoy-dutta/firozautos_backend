from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('add-expense', ExpenseViewset)
router.register('add-income', IncomeViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),

    path("upload-order-excel/", UploadStockExcelView.as_view(), name="upload-stock-excel"),
    path('purchase-report/', CombinedPurchaseView.as_view(), name="purchase-report"),
]

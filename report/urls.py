from django.urls import path,include
from .views import *

urlpatterns = [
    path('sale-report/', SaleReportView.as_view(), name='sale-report'),
    path('purchase-report/', CombinedPurchaseView.as_view(), name="purchase-report"),
    path('expense-report/', CombinedExpanseView.as_view(), name="expense-report"),
]

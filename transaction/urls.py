from django.urls import path
from .views import *



urlpatterns = [
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),

    path('purchase/', PurchaseEntryListCreateView.as_view(), name='purchase-entry-list-create'),
    path('purchase/<int:pk>/', PurchaseEntryDetailView.as_view(), name='purchase-entry-detail'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

router = DefaultRouter()

router.register(r'exporters', ExporterViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'customers', CustomerViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

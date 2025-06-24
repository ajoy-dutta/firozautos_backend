from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

router = DefaultRouter()

router.register(r'exporters', ExporterViewSet)
router.register(r'employees', EmployeeViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

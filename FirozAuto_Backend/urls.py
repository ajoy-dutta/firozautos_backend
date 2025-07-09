from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('master.urls')),
    path('api/',include('person.urls')),
    path('api/',include('Authentication.urls')),
    path('api/',include('transaction.urls')),
    path('api/', include("product.urls")),
    path('api/', include('sale.urls')),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



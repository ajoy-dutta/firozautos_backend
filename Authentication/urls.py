from django.urls import path
from .views import*
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('make-staff/<int:user_id>/', PromoteToStaffView.as_view(), name='make-staff'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("user/", CurrentUserView.as_view(), name="current-user"),

]
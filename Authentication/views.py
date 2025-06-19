from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserRegistrationSerializer(request.user)
        return Response(serializer.data)
    
class PromoteToStaffView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.is_staff:
                return Response({"message": "User is already a staff member."}, status=400)
            user.is_staff = True
            user.save()
            return Response({"message": f"{user.username} has been promoted to staff."})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow anyone to register


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return JsonResponse({'detail': 'Successfully logged out.'}, status=200)
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []  # Allow anyone to register
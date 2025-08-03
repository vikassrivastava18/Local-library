from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Book.objects.all()
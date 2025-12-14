import logging

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.serializers import BookInstanceSerializer
from catalog.models import BookInstance, Author, Book
from .serializers import UserProfileSerializer, LoadBookSerializer
from .models import UserProfile
from catalog.models import Genre
from .utils import load_books_data, extract_book_info

logger = logging.getLogger(__name__)

# Create your views here.
class CanMarkReturnedPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('catalog.can_mark_returned')


class MarkBookAsReturnedView(generics.UpdateAPIView):
    serializer_class = BookInstanceSerializer
    queryset = BookInstance.objects.all()
    permission_classes = [CanMarkReturnedPermission]


class BoorowedBooksView(generics.ListAPIView):
    serializer_class = BookInstanceSerializer
    queryset = BookInstance.objects.all()
    permission_classes = [CanMarkReturnedPermission]


class ModifyUserAccountView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [CanMarkReturnedPermission]


class LoadBookView(APIView):
    permission_classes = [CanMarkReturnedPermission]

    def post(self, request):
        serializer = LoadBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        genre_name = serializer.validated_data["genre"]
        genre = get_object_or_404(Genre, name__iexact=genre_name)

        try:
            books_data = load_books_data(genre_name)
        except FileNotFoundError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        created_count = 0

        with transaction.atomic():
            for book in books_data.get("items", []):
                book_data = extract_book_info(book)

                try:
                    Book.objects.create(
                        **book_data,
                        genre=genre
                    )
                    created_count += 1
                except IntegrityError:
                    logger.info(
                        "Duplicate ISBN skipped: %s",
                        book_data["isbn"]
                    )

        return Response(
            {
                "message": "Books loaded successfully",
                "created": created_count
            },
            status=status.HTTP_201_CREATED
        )







    
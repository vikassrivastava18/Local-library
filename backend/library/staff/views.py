import json, logging
import os, random

from django.conf import settings
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.serializers import BookInstanceSerializer
from catalog.models import BookInstance, Author, Book
from .serializers import UserProfileSerializer, LoadBookSerializer
from .models import UserProfile
from catalog.models import Genre


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

    @classmethod
    def get_books_data(cls, genre):
        try:
            # Path to JSON file
            file_path = os.path.join(
                settings.BASE_DIR,
                "book_data",
                f"{genre}.json"
            )

            if not os.path.exists(file_path):
                return Response(
                    {"error": "Book data file not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            with open(file_path, "r", encoding="utf-8") as f:
                books = json.load(f)
                return books
        except Exception as e:
            logging.ERROR(f"Error in loading JSON data: {e}, is format correct?")

    @classmethod
    def generate_isbn13(cls):
        # Generate first 12 digits
        digits = [random.randint(0, 9) for _ in range(12)]

        # Calculate checksum
        checksum = sum(
            digit * 3 if index % 2 else digit
            for index, digit in enumerate(digits)
        )
        check_digit = (10 - (checksum % 10)) % 10

        digits.append(check_digit)
        return ''.join(map(str, digits))

    @classmethod
    def get_book_info(cls, book):
        # Get the first author
        author_name = book["volumeInfo"]["authors"][0] if "authors" in book["volumeInfo"] else "Unknown"
        author_first_name = author_name.split(" ")[0]
        author_last_name = author_name.split(" ")[1] if len(author_name.split(" ")) > 1 else ""
        try:
            author = Author.objects.get(first_name=author_first_name)
        except Author.DoesNotExist:
            author = Author.objects.create(first_name=author_first_name, last_name=author_last_name)

        title = book["volumeInfo"]["title"]
        summary = book["volumeInfo"]["description"] if "description" in book["volumeInfo"] else ""
        if "industryIdentifiers" in book["volumeInfo"]:
            isbn = book["volumeInfo"]["industryIdentifiers"][0]["identifier"]
        else:
            isbn =  LoadBookView.generate_isbn13()
        cover_url = book["volumeInfo"]["imageLinks"]["thumbnail"] if "imageLinks" in book["volumeInfo"] else ""

        return {
            "author": author,
            "title": title,
            "summary": summary,
            "isbn": isbn,
            "cover_url": cover_url
        }


    def post(self, request):
        serializer = LoadBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Get genre from request
        genre = serializer.validated_data["genre"]
        genre = Genre.objects.get(name__iexact=genre)
        books = LoadBookView.get_books_data(genre)

        # count= len(books["items"])
        for book in books["items"]:
            book_data = LoadBookView.get_book_info(book)
            try:
                Book.objects.create(
                    author=book_data["author"],
                    title= book_data["title"],
                    summary= book_data["summary"],
                    isbn= book_data["isbn"],
                    cover_url= book_data["cover_url"],
                    genre = genre
                )
            except IntegrityError:
                # Duplicate ISBN – book already exists
                pass
            except Exception as e:
                pass
        return Response(
            {"message": "Resource created successfully"},
            status=status.HTTP_201_CREATED
        )









    
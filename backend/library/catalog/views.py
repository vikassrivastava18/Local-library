import logging

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Book, BookInstance, Author
from .serializers import (BookSerializer, AuthorSerializer,
                          BookInstanceSerializer, BookWithInstancesSerializer,
                          BorrowBookInstanceSerializer)

logger = logging.getLogger(__name__)

class IndexView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Home page content for the site."""
        num_books = Book.objects.count()
        num_instances = BookInstance.objects.count()
        num_authors = Author.objects.count()

        data = {
            "num_books": num_books,
            "num_instances": num_instances,
            "num_authors": num_authors
        }
        return Response(data)


class SearchBookView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, book_name):
        books = Book.objects.filter(title__icontains=book_name)
        data = {
            "books": list(books.values())
        }
        return Response(data)


class BookListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer
    paginate_by = None

    def get_queryset(self):
        genre_name = self.kwargs.get("genre")
        queryset = Book.objects.all()

        if genre_name:
            if genre_name.lower() == 'feature':
                return Book.objects.all()[:4]
            queryset = queryset.filter(
                genre__name__iexact=genre_name
            ).distinct()

        return queryset[:]


class BookDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookWithInstancesSerializer
    queryset = Book.objects.all()


class AuthorListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    paginate_by = 10
    

class AuthorDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    

class LoanedBooksListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookInstanceSerializer
    paginate_by = 10

    def get_queryset(self):
        return (BookInstance.objects.filter(borrower=self.request.user)
                .filter(status__exact='o')
                .order_by('due_back'))


class BorrowBookView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowBookInstanceSerializer
    queryset = BookInstance.objects.all()



    
    
from django.db.models import F
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Book, BookInstance, Author
from rest_framework.permissions import IsAuthenticated
from .serializers import (BookSerializer,
                          AuthorSerializer,
                          BookInstanceSerializer,
                          BookWithInstancesSerializer,
                          BorrowBookInstanceSerializer)


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
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.all()[:5]
    

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
        return (
            BookInstance.objects.filter(borrower=self.request.user)
                                .filter(status__exact='o')
                                .order_by('due_back')
        )

class BorrowBookView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowBookInstanceSerializer
    queryset = BookInstance.objects.all()

    def update(self, request, *args, **kwargs):
        # If the book is not available for loan, send error in response.
        print("Kwargs: ", kwargs)
        book_instance = BookInstance.objects.get(id=kwargs['pk'])
        if book_instance.status != 'a':
            return Response(
                {"error": "Sorry, book is not available for loan right now."},
                status=400
            )
        return super().update(request, *args, **kwargs)

    
    
from django.db.models import F
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Book, BookInstance, Author
from .serializers import BookSerializer, AuthorSerializer, BookInstanceSerializer


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


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.all()[:5]
    

class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    

class AuthorListView(generics.ListAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    paginate_by = 10
    

class AuthorDetailView(generics.RetrieveAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    

class LoanedBooksListView(generics.ListAPIView):
    serializer_class = BookInstanceSerializer
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
                                .filter(status__exact='o')
                                .order_by('due_back')
        )




    
    
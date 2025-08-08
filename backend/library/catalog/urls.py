from django.urls import path
from .views import (BookListView,
                    IndexView,
                    BookDetailView,
                    AuthorListView,
                    AuthorDetailView,
                    LoanedBooksListView,
                    MarkBookAsReturnedView,
                    BoorowedBooksView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_details'),
    path('authors/', AuthorListView.as_view(), name = 'authors'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_details'),
    path('my-books/', LoanedBooksListView.as_view(), name='loaned_books'),
    path('borrowed-books/', BoorowedBooksView.as_view(), name = 'borrowed_books'),
    path('mark-returned/<uuid:pk>/', MarkBookAsReturnedView.as_view(), name='mark_book_returned')
]

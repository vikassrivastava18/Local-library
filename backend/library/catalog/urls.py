from django.urls import path
from .views import (BookListView, IndexView,
                    BookDetailView, AuthorListView,
                    AuthorDetailView, LoanedBooksListView,
                    BorrowBookView, SearchBookView, UserBookHistory,
                    )

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('books-list/<str:genre>/', BookListView.as_view(), name='books'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_details'),
    path('authors/', AuthorListView.as_view(), name = 'authors'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_details'),
    path('my-books/', LoanedBooksListView.as_view(), name='loaned_books'),
    path('borrow-book/<str:pk>', BorrowBookView.as_view(), name='borrow_book'),
    path('search-book/<str:book_name>', SearchBookView.as_view(), name='search_book'),
    path('user-book-list', UserBookHistory.as_view(), name='user_book_list'),
]

from django.urls import path
from .views import (MarkBookAsReturnedView,
                    BoorowedBooksView,
                    ModifyUserAccountView)


urlpatterns = [
    path('borrowed-books/', BoorowedBooksView.as_view(), name = 'borrowed_books'),
    path('mark-returned/<uuid:pk>/', MarkBookAsReturnedView.as_view(), name='mark_book_returned'),
    path('update-user-status/<int:pk>/', ModifyUserAccountView.as_view(), name='update_user_profile')
]

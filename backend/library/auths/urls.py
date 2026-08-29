
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistrationView, LogoutView


urlpatterns = [
    path('login/', obtain_auth_token, name='api-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register-user'),
]


    
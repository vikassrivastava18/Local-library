from django.urls import path

from .views import logging

urlpatterns = [
    path('logging', logging, name='logging'),

]
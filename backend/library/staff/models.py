from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import Book

from catalog.models import BookInstance


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), primary_key=True, on_delete=models.CASCADE)
    USER_STATUS = (
        ('a', 'Active'),
        ('b', 'Blocked')
    )
    status = models.CharField(
        max_length=1,
        choices=USER_STATUS,
        default='a',
        help_text='User account status'
    )
    address = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)


class BookInstanceHistory(models.Model):
    book_instance = models.CharField(max_length=64)
    status = models.CharField(max_length=1)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

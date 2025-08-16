from django.contrib import admin
from .models import UserProfile, BookInstanceHistory
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(BookInstanceHistory)
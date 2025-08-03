from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class UserDetail(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status_choices = (
        ('ac', 'Active'),
        ('in', 'Inactive'),
        ('pe', 'Pending'),
        ('bl', 'Blocked')
    )
    status = models.CharField(
        max_length=2,
        choices=status_choices,
        default='pe'
    )
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"User: {self.user.username}, Phone: {self.phone}, Address: {self.address[:20]}"
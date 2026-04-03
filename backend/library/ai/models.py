from django.db import models

from django.contrib.auth import get_user_model


# Create your models here.
class Request(models.Model):
    request = models.CharField(max_length=512)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.request}" if self.user else f"{self.request}"
    

class Complain(models.Model):
    complain = models.CharField(max_length=512)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.complain}" if self.user else f"{self.complain}"




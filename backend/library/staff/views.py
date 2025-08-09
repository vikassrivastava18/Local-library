from rest_framework import generics
from rest_framework.permissions import BasePermission

from catalog.serializers import BookInstanceSerializer
from catalog.models import BookInstance
from .serializers import UserProfileSerializer
from .models import UserProfile
# Create your views here.


class CanMarkReturnedPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('catalog.can_mark_returned')


class MarkBookAsReturnedView(generics.UpdateAPIView):
    permission_classes = [CanMarkReturnedPermission]
    serializer_class = BookInstanceSerializer
    queryset = BookInstance.objects.all()


class BoorowedBooksView(generics.ListAPIView):
    permission_classes = [CanMarkReturnedPermission]
    serializer_class = BookInstanceSerializer
    queryset = BookInstance.objects.all()


class ModifyUserAccountView(generics.UpdateAPIView):
    permission_classes = [CanMarkReturnedPermission]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
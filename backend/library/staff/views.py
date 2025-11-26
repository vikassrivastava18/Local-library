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
    serializer_class = BookInstanceSerializer
    queryset = BookInstance.objects.all()
    permission_classes = [CanMarkReturnedPermission]


class BoorowedBooksView(generics.ListAPIView):
    serializer_class = BookInstanceSerializer
    queryset = BookInstance.objects.all()
    permission_classes = [CanMarkReturnedPermission]


class ModifyUserAccountView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [CanMarkReturnedPermission]

    
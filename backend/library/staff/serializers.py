from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Validation rules same as defined in the UserProfile model
    """
    class Meta:
        model = UserProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance
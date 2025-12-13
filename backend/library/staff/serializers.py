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


class LoadBookSerializer(serializers.Serializer):
    genre = serializers.CharField()

    ALLOWED_GENRES = {"fiction", "history", "biography", "science", "philosophy"}

    def validate_genre(self, value):
        value = value.lower()
        if value not in self.ALLOWED_GENRES:
            raise serializers.ValidationError(
                "Genre must be one of: fiction, history, biography"
            )
        return value

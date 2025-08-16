from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # use proper field types; keep password write-only
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ("username", "email", "password")
        # disable DRF's auto UniqueValidator so *your* checks run
        extra_kwargs = {
            "username": {"validators": []},
            "email": {"validators": []},
        }
        # also disable any model-level validators that could short-circuit
        validators = []

    # --- field-level validators (DRF aggregates these automatically) ---

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value or "") < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def create(self, validated_data):
        # let DB unique constraints still protect you, but by now we’ve validated
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from .models import Book, Author, BookInstance


class BookSerializer(serializers.ModelSerializer):
    """
        Serializer for a book. 
        Validation rules same as that defined in the model Book.
    """
    
    author_name = serializers.SerializerMethodField(read_only=True)

    def get_author_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookInstanceSerializer(serializers.ModelSerializer):
    borrower_name = serializers.CharField(source='borrower.username', read_only=True)
    status_display = serializers.SerializerMethodField(read_only=True)

    def get_status_display(self, obj):
        return obj.get_status_display()
    
    class Meta:
        model = BookInstance
        fields = '__all__'

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    

class BorrowBookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = []

    def validate(self, attrs):
        """Validate before update is called"""
        instance = self.instance
        if instance.status != 'a':
            raise ValidationError(
                {"error": "Sorry, the book is not available for loan right now."}
            )
        return attrs

    def update(self, instance, validated_data):
        user = self.context['request'].user # The current user
        instance.status = 'o'  # Assuming 'o' is the code for "on loan"
        borrow_till = settings.BORROW_DAYS_COUNT
        due_date = timezone.now().date() + timedelta(days=borrow_till)
        instance.due_back = due_date
        instance.borrower = user    # Assign current user as borrower
        instance.save()
        return instance
    

class BookWithInstancesSerializer(serializers.ModelSerializer):
    instances = BookInstanceSerializer(source='bookinstance_set', many=True, read_only=True)
    author_name = serializers.SerializerMethodField(read_only=True)

    def get_author_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    class Meta:
        model = Book
        fields = '__all__'


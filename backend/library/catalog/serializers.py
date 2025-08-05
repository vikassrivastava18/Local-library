from rest_framework import serializers
from .models import Book, Author


class BookSerializer(serializers.ModelSerializer):
    """
        Serializer for validating a book. 
        Validation rules same as that defined in the model Book.
    """
    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
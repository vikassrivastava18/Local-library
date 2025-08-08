from rest_framework import serializers
from .models import Book, Author, BookInstance


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


class BookInstanceSerializer(serializers.ModelSerializer):
    borrower_name = serializers.CharField(source='borrower.username', read_only=True)
    
    class Meta:
        model = BookInstance
        fields = '__all__'
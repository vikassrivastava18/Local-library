from rest_framework import serializers
from .models import Book, Author, BookInstance


class BookSerializer(serializers.ModelSerializer):
    """
        Serializer for a book. 
        Validation rules same as that defined in the model Book.
    """
    book_author = serializers.CharField(source='author.first_name', read_only=True)

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

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance
from django.db import models
from django.urls import reverse # Used in get_absolute_url() to get URL for the specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of a field
# Create your models here.

class Genre(models.Model):
    """Model represents the genre(adventure, romance, etc.)"""

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter the book genre (eg. Science Fiction, Poetry etc.)"
    )

    def __str__(self):
        return self.name[:50]
    
    def get_absolute_url(self):
        """Return the URL to access a particular genre instance."""
        return reverse("genre-detail", args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name="genre_name_case_insensitive_unique",
                violation_error_message= "Genre already exists (case insinsitive match)"
            )
        ]


class Book(models.Model):
    """Model reprenting a book (but not a specific copy)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief descritipn of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select one or more genre for this book.")

    LANGUAGE_OPTIONS = (
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('ta', 'Tamil')
    )

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_OPTIONS,
        default= 'en',
        help_text='Book Language',
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('title'),
                name = "book_name_case_insensitive_unique",
                violation_error_message="Book name already exists (case insinsitive match)"
            )
        ]


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


import uuid # Required for unique book instances

class BookInstance(models.Model):

    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

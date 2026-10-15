from datetime import date, datetime, timedelta, timezone as datetime_timezone
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Author, Book, BookInstance, Genre


class BorrowBookViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="borrower",
        )
        author = Author.objects.create(first_name="Test", last_name="Author")
        genre = Genre.objects.create(name="Test Genre")
        book = Book.objects.create(
            title="Test Book",
            author=author,
            summary="A book for borrowing tests.",
            isbn="1234567890123",
            genre=genre,
        )
        self.book_instance = BookInstance.objects.create(
            book=book,
            imprint="Test imprint",
            status="a",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.borrow_url = reverse(
            "borrow_book",
            kwargs={"pk": str(self.book_instance.pk)},
        )

    def test_only_available_books_can_be_borrowed(self):
        for status in ("m", "o", "r"):
            with self.subTest(status=status):
                self.book_instance.status = status
                self.book_instance.save(update_fields=["status"])

                response = self.client.put(self.borrow_url, {})

                self.assertEqual(response.status_code, 400)
                self.book_instance.refresh_from_db()
                self.assertEqual(self.book_instance.status, status)

        self.book_instance.status = "a"
        self.book_instance.save(update_fields=["status"])

        response = self.client.put(self.borrow_url, {})

        self.assertEqual(response.status_code, 200)
        self.book_instance.refresh_from_db()
        self.assertEqual(self.book_instance.status, "o")
        self.assertEqual(self.book_instance.borrower, self.user)

    @patch(
        "catalog.serializers.timezone.now",
        return_value=datetime(2025, 1, 1, tzinfo=datetime_timezone.utc),
    )
    def test_borrowed_book_duration_does_not_exceed_maximum(self, _mock_now):
        response = self.client.put(self.borrow_url, {})

        self.assertEqual(response.status_code, 200)
        self.book_instance.refresh_from_db()
        maximum_due_date = date(2025, 1, 1) + timedelta(
            days=settings.BORROW_DAYS_COUNT
        )
        self.assertEqual(self.book_instance.due_back, maximum_due_date)
        self.assertLessEqual(
            (self.book_instance.due_back - date(2025, 1, 1)).days,
            settings.BORROW_DAYS_COUNT,
        )

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from catalog.models import Author, Book, BookInstance, Genre


class StaffViewPermissionsTest(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.regular_user = user_model.objects.create_user(
            username="regular-user",
            password="test-password",
        )
        self.staff_user = user_model.objects.create_user(
            username="library-staff",
            password="test-password",
        )
        permission = Permission.objects.get(
            content_type__app_label="catalog",
            codename="can_mark_returned",
        )
        self.staff_user.user_permissions.add(permission)

        author = Author.objects.create(first_name="Test", last_name="Author")
        self.genre = Genre.objects.create(name="fiction")
        self.book = Book.objects.create(
            title="Test Book",
            author=author,
            summary="A book for staff endpoint tests.",
            isbn="1234567890123",
            genre=self.genre,
        )
        self.book_instance = BookInstance.objects.create(
            book=self.book,
            imprint="Test imprint",
            borrower=self.regular_user,
            status="o",
        )
        self.client = APIClient()

    def test_only_staff_can_mark_book_as_returned(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.patch(
            reverse(
                "mark_book_returned",
                kwargs={"pk": self.book_instance.pk},
            ),
            {"status": "a"},
        )

        self.assertEqual(response.status_code, 403)
        self.book_instance.refresh_from_db()
        self.assertEqual(self.book_instance.status, "o")

    def test_staff_can_mark_book_as_returned(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.patch(
            reverse(
                "mark_book_returned",
                kwargs={"pk": self.book_instance.pk},
            ),
            {"status": "a"},
        )

        self.assertEqual(response.status_code, 200)
        self.book_instance.refresh_from_db()
        self.assertEqual(self.book_instance.status, "a")

    def test_only_staff_can_access_load_book(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.post(
            reverse("load_book"),
            {"genre": "fiction"},
        )

        self.assertEqual(response.status_code, 403)

    @patch("staff.views.LoadBookView.get_books_data", return_value={"items": []})
    def test_staff_can_access_load_book(self, _mock_get_books_data):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.post(
            reverse("load_book"),
            {"genre": "fiction"},
        )

        self.assertEqual(response.status_code, 201)

    def test_only_staff_can_create_book_instances(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.post(reverse("create_book_instances"))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            BookInstance.objects.filter(book=self.book).count(),
            1,
        )

    def test_staff_can_create_book_instances(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.post(reverse("create_book_instances"))

        self.assertEqual(response.status_code, 201)
        instances = BookInstance.objects.filter(book=self.book)
        self.assertEqual(instances.count(), 5)
        # self.assertTrue(
        #     all(instance.borrower == self.staff_user for instance in instances)
        # )

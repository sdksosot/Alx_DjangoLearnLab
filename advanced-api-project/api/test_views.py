from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from .models import Author, Book


class BookAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass1234")

        self.client = APIClient()  # unauthenticated
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user)

        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        self.book1 = Book.objects.create(title="Utopia", publication_year=2008, author=self.author1)
        self.book2 = Book.objects.create(title="Legend of X", publication_year=1993, author=self.author1)
        self.book3 = Book.objects.create(title="Another Tale", publication_year=2015, author=self.author2)

        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')

    def test_list_books_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # استخدام response.data بدلاً من json()
        self.assertGreaterEqual(len(response.data), 3)

    def test_retrieve_book_detail(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['title'], self.book1.title)
        self.assertEqual(data['publication_year'], self.book1.publication_year)

    def test_create_book_authenticated(self):
        payload = {"title": "Created by Test", "publication_year": 2021, "author": self.author1.pk}
        response = self.auth_client.post(self.create_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertEqual(data['title'], payload['title'])
        self.assertEqual(data['publication_year'], payload['publication_year'])
        self.assertTrue(Book.objects.filter(pk=data['id']).exists())

    def test_update_book_authenticated(self):
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        payload = {"title": "Utopia Edited", "publication_year": 2008, "author": self.author1.pk}
        response = self.auth_client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Utopia Edited")

    def test_delete_book_authenticated(self):
        url = reverse('book-delete', kwargs={'pk': self.book2.pk})
        response = self.auth_client.delete(url)
        self.assertIn(response.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    def test_filter_by_publication_year(self):
        response = self.client.get(self.list_url, {'publication_year': 2015})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], self.book3.title)

    def test_search_by_title_or_author(self):
        response = self.client.get(self.list_url, {'search': 'Legend'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        self.assertTrue(any('Legend' in item['title'] for item in results))

    def test_ordering_by_publication_year(self):
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        years = [item['publication_year'] for item in results]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_publication_year_validation_on_create(self):
        future_year = 3000
        payload = {"title": "Future Book", "publication_year": future_year, "author": self.author1.pk}
        response = self.auth_client.post(self.create_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from .models import Author, Book


class BookAPITestCase(TestCase):
    """
    اختبار نقاط النهاية (endpoints) للـ Book:
    - CRUD (create, retrieve, update, delete)
    - الفلترة، البحث، والفرز (filter/search/ordering)
    - التحقق من الصلاحيات (authenticated vs unauthenticated)
    """

    def setUp(self):
        # مستخدم تجريبي مسجّل
        self.user = User.objects.create_user(username="tester", password="pass1234")

        # عملاء API (واحد للاختبارات غير المصرّح بها وآخر للمصرّح به)
        self.client = APIClient()  # غير مصرح
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user)  # مصرح

        # بيانات تجريبية: مؤلفان وعدد من الكتب
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # كتب متعددة لتجارب الفلترة والبحث والفرز
        self.book1 = Book.objects.create(title="Utopia", publication_year=2008, author=self.author1)
        self.book2 = Book.objects.create(title="Legend of X", publication_year=1993, author=self.author1)
        self.book3 = Book.objects.create(title="Another Tale", publication_year=2015, author=self.author2)

        # نقاط النهاية (اعتماداً على api/urls.py كما وضعناه سابقاً)
        self.list_url = reverse('book-list')            # /api/books/
        self.create_url = reverse('book-create')        # /api/books/create/

    def test_list_books_unauthenticated(self):
        """GET /api/books/ يجب أن يعود 200 ويحتوي على الكتب الموجودة"""
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # نتأكد أن عدد النتائج >= 3
        self.assertGreaterEqual(len(resp.json()), 3)

    def test_retrieve_book_detail(self):
        """GET /api/books/<pk>/ يجب إرجاع بيانات الكتاب المطلوبة"""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data['title'], self.book1.title)
        self.assertEqual(data['publication_year'], self.book1.publication_year)

    def test_create_book_requires_authentication(self):
        """POST لإنشاء كتاب بدون مصادقة يجب أن يرفض (401 أو 403 حسب الإعداد)"""
        payload = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author1.pk
        }
        resp = self.client.post(self.create_url, data=payload, format='json')
        # التحقق: غير مصرح، ننتظر 401 أو 403 (DRF غالباً 401 لل non-authenticated)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """POST مصدق يجب أن ينشئ كتابًا جديدًا ويُعيد 201"""
        payload = {
            "title": "Created by Test",
            "publication_year": 2021,
            "author": self.author1.pk
        }
        resp = self.auth_client.post(self.create_url, data=payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        self.assertEqual(data['title'], payload['title'])
        self.assertEqual(data['publication_year'], payload['publication_year'])
        # نتأكد أن الكتاب موجود في DB
        self.assertTrue(Book.objects.filter(pk=data['id']).exists())

    def test_update_book_requires_authentication(self):
        """PUT بدون مصادقة يجب أن يُمنع"""
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        payload = {"title": "Attempted Update", "publication_year": 2009, "author": self.author1.pk}
        resp = self.client.put(url, data=payload, format='json')
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated(self):
        """PUT مصدق يجب أن يحدث بيانات الكتاب"""
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        payload = {"title": "Utopia Edited", "publication_year": 2008, "author": self.author1.pk}
        resp = self.auth_client.put(url, data=payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Utopia Edited")

    def test_delete_book_requires_authentication(self):
        """DELETE بدون مصادقة يجب أن يُمنع"""
        url = reverse('book-delete', kwargs={'pk': self.book2.pk})
        resp = self.client.delete(url)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        # الكتاب لازال موجودًا
        self.assertTrue(Book.objects.filter(pk=self.book2.pk).exists())

    def test_delete_book_authenticated(self):
        """DELETE مصدق يجب أن يزيل الكتاب ويُعيد 204"""
        url = reverse('book-delete', kwargs={'pk': self.book2.pk})
        resp = self.auth_client.delete(url)
        # بعض إعدادات DRF تعيد 204 No Content عند الحذف
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    def test_filter_by_publication_year(self):
        """فلترة بالعام: ?publication_year=2015 يجب أن يرجع الكتاب المناسب"""
        resp = self.client.get(self.list_url, {'publication_year': 2015})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.json()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], self.book3.title)

    def test_search_by_title_or_author(self):
        """بحث نصي ?search=Legend يجب أن يرجع كتاب 'Legend of X'"""
        resp = self.client.get(self.list_url, {'search': 'Legend'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.json()
        # يجب أن يعود على الأقل كتاب واحد يحمل الكلمة 'Legend'
        self.assertTrue(any('Legend' in item['title'] for item in results))

    def test_ordering_by_publication_year(self):
        """الفرز ?ordering=-publication_year يجب أن يعيد الكتب بالتنازلي حسب السنة"""
        resp = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.json()
        years = [item['publication_year'] for item in results]
        # التحقق أن القائمة مرتبة تنازلياً
        self.assertEqual(years, sorted(years, reverse=True))

    def test_publication_year_validation_on_create(self):
        """محاولة إنشاء كتاب بسنة مستقبلية يجب أن تفشل (validated in serializer)"""
        future_year = 3000
        payload = {"title": "Future Book", "publication_year": future_year, "author": self.author1.pk}
        resp = self.auth_client.post(self.create_url, data=payload, format='json')
        # التحقق: خطأ في التحقق من الصحة (400 Bad Request)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', resp.json())

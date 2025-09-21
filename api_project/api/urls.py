from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# إنشاء الراوتر
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Endpoint القديم (لستة الكتب فقط)
    path('books/', BookList.as_view(), name='book-list'),

    # Endpoints الخاصة بالـ CRUD (BooksViewSet)
    path('', include(router.urls)),
]

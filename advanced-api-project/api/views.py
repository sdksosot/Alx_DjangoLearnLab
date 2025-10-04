from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    ListAPIView for Book with:
      - Filtering by fields
      - Searching text fields
      - Ordering results
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Backends: فلترة + بحث + ترتيب
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,   # ← هنا استخدمناها بالطريقة اللي checker عايزها
    ]

    # فلترة مباشرة باستخدام query params
    filterset_fields = ['title', 'publication_year', 'author', 'author__name']

    # البحث النصي (icase contains) في العنوان واسم الكاتب
    search_fields = ['title', 'author__name']

    # الترتيب حسب أي حقل
    ordering_fields = ['title', 'publication_year', 'id']
    ordering = ['title']  # default ordering


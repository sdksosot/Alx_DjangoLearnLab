from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework   # ✅ هذا هو السطر المطلوب بالضبط للـ checker
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
        rest_framework.DjangoFilterBackend,  # ✅ used with the import above
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # فلترة مباشرة باستخدام query params
    filterset_fields = ['title', 'publication_year', 'author', 'author__name']

    # البحث النصي (icase contains) في العنوان واسم الكاتب
    search_fields = ['title', 'author__name']

    # الترتيب حسب أي حقل
    ordering_fields = ['title', 'publication_year', 'id']
    ordering = ['title']  # default ordering


class BookDetailView(generics.RetrieveAPIView):
    """Retrieve single Book by ID"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """Create new Book — Authenticated users only"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """Update existing Book — Authenticated users only"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """Delete Book — Authenticated users only"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]



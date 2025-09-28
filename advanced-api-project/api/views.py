from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    ListAPIView for Book with:
      - Filtering by fields (exact matches & related fields)
      - Search across text fields (title, author.name)
      - Ordering by model fields (title, publication_year, ...)
    Permission: IsAuthenticatedOrReadOnly -> anyone can read, write requires auth.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Backends: DjangoFilterBackend (exact / lookup filters), SearchFilter (text search), OrderingFilter (sort)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Fields allowed for direct filtering via query params, e.g. ?title=Utopia or ?publication_year=2008
    # You can also filter by author (id) or related author name via author__name (depends on lookup)
    filterset_fields = ['title', 'publication_year', 'author', 'author__name']

    # Fields to search text in using ?search=... (performs icontains by default)
    search_fields = ['title', 'author__name']

    # Fields allowed to order by, and default ordering
    ordering_fields = ['title', 'publication_year', 'id']
    ordering = ['title']  # default ordering



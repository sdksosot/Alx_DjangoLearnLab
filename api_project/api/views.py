from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# القديم (ListAPIView)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# الجديد (CRUD كامل باستخدام ViewSet)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # ← لازم يكون مسجل دخول





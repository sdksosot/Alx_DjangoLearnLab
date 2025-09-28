from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# ListView: عرض جميع الكتب (مسموح للجميع)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # قراءة فقط مسموح بها للجميع


# DetailView: عرض كتاب محدد بالـ ID (مسموح للجميع)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# CreateView: إضافة كتاب جديد (مسموح فقط للمستخدمين المسجلين)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # لازم تسجيل دخول


# UpdateView: تعديل بيانات كتاب موجود (مسموح فقط للمستخدمين المسجلين)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # تخصيص سلوك التحديث (مثال: منع تغيير السنة لسنة مستقبلية - تم التحقق منها أصلاً بالـ serializer)
    def perform_update(self, serializer):
        serializer.save()


# DeleteView: حذف كتاب (مسموح فقط للمستخدمين المسجلين)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


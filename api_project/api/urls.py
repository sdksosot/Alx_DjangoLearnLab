from django.urls import path
from .views import BookList   # هنا بنتأكد إننا مستوردين BookList

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
]

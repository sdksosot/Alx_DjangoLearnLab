from rest_framework import serializers
from .models import Author, Book
import datetime


# BookSerializer:
# يقوم بتحويل بيانات الكتاب إلى JSON والعكس
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom Validation: لا يسمح بسنة نشر أكبر من السنة الحالية
    def validate_publication_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# AuthorSerializer:
# يقوم بتحويل بيانات الكاتب إلى JSON مع تضمين الكتب بشكل متداخل (nested)
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer لعرض الكتب الخاصة بالكاتب
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

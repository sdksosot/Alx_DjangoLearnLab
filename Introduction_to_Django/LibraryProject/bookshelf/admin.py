from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")  # الأعمدة اللي تظهر
    list_filter = ("publication_year", "author")            # علشان تعمل فلترة
    search_fields = ("title", "author")                     # هنا بتعمل بحث بالعنوان أو الكاتب

admin.site.register(Book, BookAdmin)

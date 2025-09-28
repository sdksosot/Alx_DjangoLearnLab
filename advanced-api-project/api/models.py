from django.db import models

# Author Model:
# يمثل كاتب يمكن أن يكون له أكثر من كتاب (one-to-many)
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Book Model:
# يمثل كتاب مرتبط بكاتب واحد
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    # علاقة One-to-Many: كل كتاب مرتبط بكاتب واحد
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
 
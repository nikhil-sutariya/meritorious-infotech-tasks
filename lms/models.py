from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=150)
    birth_date = models.DateField()

    class Meta:
        db_table = "author"
        verbose_name = "Author"
        verbose_name_plural = "Authors"
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    class Meta:
        db_table = "book"
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title

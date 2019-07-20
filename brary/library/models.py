from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    author_last_name = models.CharField(max_length=25)
    author_first_name = models.CharField(max_length=25)

    def __str__(self):
        return self.author_last_name + ", " + self.author_first_name

class Book(models.Model):
    book_author = models.ForeignKey(Author,on_delete=models.CASCADE)
    book_owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    book_title = models.CharField(max_length=100)
    book_descr = models.CharField(max_length=2000)
    book_publish_date = models.DateTimeField('date published')
    # TODO: Look at img field
    book_img = models.CharField(max_length=500, default="")


    book_available = models.BooleanField(default=True)

    def __str__(self):
        return self.book_title

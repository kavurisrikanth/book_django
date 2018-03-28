from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateField('date published')
    isbn = models.CharField(max_length=15, primary_key=True, default='isbnPlaceholder')
    author = models.CharField(max_length=100, default='authorPlaceholder')
    small_img = models.CharField(max_length=200, default='smallImgPlaceholder')
    large_img = models.CharField(max_length=200, default='largeImgPlaceholder')
    description = models.CharField(max_length=2000, default='descriptionPlaceholder')
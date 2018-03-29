from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateField('date published')
    isbn = models.CharField('ISBN', max_length=15, primary_key=True, default='isbnPlaceholder')
    author = models.CharField(max_length=100, default='authorPlaceholder')
    price = models.FloatField(default=-1.0)
    for_sale = models.BooleanField(default=False)
    # author = models.ManyToManyField('Author')
    small_img = models.CharField(max_length=200, default='smallImgPlaceholder')
    large_img = models.CharField(max_length=200, default='largeImgPlaceholder')
    description = models.TextField(max_length=2000, default='descriptionPlaceholder')

# class Author(models.Model):
#     name = models.CharField(max_length=100)
#
#     class Meta:
#         ordering = ['name']
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

class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, default=None)

class Order(models.Model):
    placed_date = models.DateTimeField('date placed')
    total_amount = models.FloatField(default=0.0)
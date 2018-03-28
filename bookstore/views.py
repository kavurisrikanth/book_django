from django.shortcuts import render
import os, json, datetime
from django.conf import settings
from .models import Book
from django.core import serializers
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    with open(os.path.join(settings.STATIC_ROOT, 'bookstore/books.json')) as jsonFile:
        jsonData = json.load(jsonFile)

    insertDataIfNeeded(jsonData)

    jsonStr = serializers.serialize('json', Book.objects.all())
    # print (jsonStr)
    # print(type(jsonStr))

    context = {
        'jsonString': jsonStr
    }
    return render(request, 'bookstore/index.html', context)
	# return HttpResponse('Welcome to the index page of the bookstore!')


def viewBook(request):
    isbn = request.GET['isbn']
    jsonStr = serializers.serialize('json', [Book.objects.get(pk=isbn),])

    print('json str: ' + jsonStr)

    context = {
        'jsonString': jsonStr
    }
    return render(request, 'bookstore/viewbook.html', context)


def addToCart(request):
    return HttpResponseRedirect(reverse('bookstore:index'))

# Helper functions
def insertDataIfNeeded(jsonData):
    print('Entered function')

    # if len(Book.objects.all()) == len(jsonData['items']):
    #     return

    print ('About to check data')

    # bookData will be a dictionary
    for bookData in jsonData['items']:
        indID = (bookData['volumeInfo'])['industryIdentifiers']
        title = (bookData['volumeInfo'])['title']
        author = ((bookData['volumeInfo'])['authors'])[0]

        dateStr = (bookData['volumeInfo'])['publishedDate']
        [year, month, day] = createDateFromString(dateStr)

        pubDate = datetime.date(int(year), int(month), int(day))

        # indID will be a list
        for idData in indID:
            if idData['type'] == 'ISBN_13':
                isbn = idData['identifier']
                print('ISBN 13 found: ' + isbn)
                try:
                    bookObj = Book.objects.get(pk=isbn)
                    print('Book exists')
                    print('title: ' + bookObj.title)
                    checkBookData(bookObj, bookData)
                except Book.DoesNotExist:
                    newBook = Book(title=title, pub_date=pubDate, isbn=isbn, author=author)
                    newBook.save()
                    print('Book inserted')


def createDateFromString(dateStr):
    datePieces = dateStr.split('-')

    if len(datePieces) == 0:
        year = '1970'
        month = '01'
        day = '01'
    if len(datePieces) == 1:
        [year] = datePieces
        month = '01'
        day = '01'
    if len(datePieces) == 2:
        [year, month] = datePieces
        day = '01'
    if len(datePieces) == 3:
        [year, month, day] = datePieces

    return [year, month, day]

'''
This function checks the data of ONE book. If there are any discrepancies, they are fixed.
'''
def checkBookData(bookFromDB, jsonBookData):
    altered = False

    if bookFromDB.title != (jsonBookData['volumeInfo'])['title']:
        bookFromDB.title = (jsonBookData['volumeInfo'])['title']
        altered = True

    if bookFromDB.author != ((jsonBookData['volumeInfo'])['authors'])[0]:
        bookFromDB.author = ((jsonBookData['volumeInfo'])['authors'])[0]
        altered = True

    if bookFromDB.small_img != ((jsonBookData['volumeInfo'])['imageLinks'])['smallThumbnail']:
        bookFromDB.small_img = ((jsonBookData['volumeInfo'])['imageLinks'])['smallThumbnail']
        altered = True

    if bookFromDB.large_img != ((jsonBookData['volumeInfo'])['imageLinks'])['thumbnail']:
        bookFromDB.large_img = ((jsonBookData['volumeInfo'])['imageLinks'])['thumbnail']
        altered = True

    targetDesc = ((jsonBookData['volumeInfo'])['description']).replace('\"', '\'')
    if bookFromDB.description != targetDesc:
        bookFromDB.description = targetDesc
        altered = True

    if altered:
        bookFromDB.save()

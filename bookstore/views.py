from django.shortcuts import render
import os, json, datetime
from django.conf import settings
from .models import Book, BookInstance, Order
from django.core import serializers
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def index(request):
    return HttpResponseRedirect(reverse('bookstore:home'))

def home(request):
    with open(os.path.join(settings.STATIC_ROOT, 'bookstore/books.json')) as jsonFile:
        jsonData = json.load(jsonFile)

    insertDataIfNeeded(jsonData)

    jsonStr = serializers.serialize('json', Book.objects.all())

    print (jsonStr)
    # print(type(jsonStr))
    cartContents = request.session.get('cartContents', {})
    cartSize = len(cartContents)

    context = {
        'jsonString': jsonStr,
        'cartSize': cartSize
    }
    return render(request, 'bookstore/home.html', context)
	# return HttpResponse('Welcome to the index page of the bookstore!')


def viewBook(request):
    isbn = request.GET['isbn']
    jsonStr = serializers.serialize('json', [Book.objects.get(pk=isbn),])

    print('json str: ' + jsonStr)
    cartContents = request.session.get('cartContents', {})
    cartSize = len(cartContents)

    context = {
        'jsonString': jsonStr,
        'cartSize': cartSize
    }
    return render(request, 'bookstore/viewbook.html', context)


def addToCart(request):
    from django.contrib import messages

    # Get the current cart contents from the session

    print('\n\n')
    for key in request.POST:
        print(key + ' -> ' + request.POST[key])

    cartContents = request.session.get('cartContents', {})
    selectedIsbn = request.POST['isbn_input']
    selectedQuantity = int(request.POST['quantity'])


    if selectedIsbn not in cartContents:
        cartContents[selectedIsbn] = 0

    errorMsg = ''
    if cartContents[selectedIsbn] + selectedQuantity <= 3:
        cartContents[selectedIsbn] += selectedQuantity
        request.session['cartContents'] = cartContents
        request.session.modified = True
        copy = 'copies' if cartContents[selectedIsbn] > 1 else 'copy'
        has = 'have' if cartContents[selectedIsbn] > 1 else 'has'
        successMsg = str(cartContents[selectedIsbn]) + ' ' + copy + ' of "' + Book.objects.get(pk=selectedIsbn).title + '" ' + has + ' been added to your cart.'
        messages.success(request, successMsg)
    else:
        errorMsg = 'You may only add a maximum of 3 copies of each book to your cart.'
        messages.error(request, errorMsg)

    return HttpResponseRedirect(reverse('bookstore:index'))


def viewCart(request):
    # import json

    cartContents = request.session.get('cartContents', {})
    # cartData = serializers.serialize('json', [])
    jsonStr = ''
    if cartContents:
        bookData = []
        for isbn in cartContents.keys():
            # isbn = (key.split('_'))[1]
            bookData.append(Book.objects.get(pk=isbn))
        jsonStr = serializers.serialize('json', bookData)

    return render(request, 'bookstore/cart.html', {
        'jsonString': jsonStr,
        'cartData': json.dumps(cartContents),
        'cartSize': len(cartContents)
    })
    # return HttpResponseRedirect(reverse('bookstore:index'))


def pay(request):
    cartContents = request.session.get('cartContents', {})
    if cartContents:
        totalAmt = 0
        newOrder = Order(placed_date=datetime.datetime.now())
        newOrder.save()
        for isbn in cartContents.keys():
            quantity = cartContents[isbn]
            newBookInstance = BookInstance(isbn=Book.objects.get(pk=isbn), quantity=quantity, order=newOrder)
            newBookInstance.save()
            totalAmt += (quantity * Book.objects.get(pk=isbn).price)

        newOrder.total_amount = totalAmt
        newOrder.save()

        cartContents.clear()
        request.session['cartContents'] = cartContents
        request.session.modified = True
    return render(request, 'bookstore/pay.html')


def orderHistory(request):
    cartContents = request.session.get('cartContents', {})
    try:
        orderId = request.GET['order_id']
        thisOrder = Order.objects.get(id=orderId)

        bookList = []
        for bookObj in thisOrder.bookinstance_set.all():
            # print('isbn: ' + bookObj.isbn)
            bookList.append(bookObj.isbn)
        context = {
            'orderDetails': serializers.serialize('json', [thisOrder,]),
            'bookList': serializers.serialize('json', bookList),
            'cartSize': len(cartContents)
        }
        return render(request, 'bookstore/vieworders.html', context)
    except KeyError:
        context = {
            'orderHistory': Order.objects.all(),
            'cartSize': len(cartContents)
        }
        return render(request, 'bookstore/vieworders.html', context)

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

        # checkAuthorData((bookData['volumeInfo'])['authors'])

        dateStr = (bookData['volumeInfo'])['publishedDate']
        [year, month, day] = createDateFromString(dateStr)

        pubDate = datetime.date(int(year), int(month), int(day))

        # indID will be a list
        for idData in indID:
            if idData['type'] == 'ISBN_13':
                isbn = idData['identifier']
                print('ISBN 13 found: ' + isbn)
                try:
                    print('looking for book with ISBN: ' + isbn)
                    bookObj = Book.objects.get(pk=isbn)
                    print('Book exists')
                    print('title: ' + bookObj.title)
                    checkBookData(bookObj, bookData)
                except Book.DoesNotExist:
                    newBook = Book(title=title, pub_date=pubDate, isbn=isbn, author=author)
                    newBook.save()

                    # for authorName in (bookData['volumeInfo'])['authors']:
                    #     print('looking for author named: ' + authorName)
                    #     newBook.author.create(name=authorName)
                    #     # newBook.author.add(authorName)
                    # newBook.save()
                    print('Book inserted')
                    checkBookData(newBook, bookData)


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

    forSale = (jsonBookData['saleInfo'])['saleability'] == 'FOR_SALE'
    if forSale and (not bookFromDB.for_sale):
        bookFromDB.for_sale = True
        altered = True

    if forSale:
        targetAmt = ((jsonBookData['saleInfo'])['retailPrice'])['amount']
        if bookFromDB.price != targetAmt:
            bookFromDB.price = targetAmt
            altered = True

    if altered:
        bookFromDB.save()


'''
Check if this list of authors is present in the Author table.
If any one isn't, then insert it.

Scrapped.
'''
# def checkAuthorData(authorList):
#     for authorName in authorList:
#         try:
#             print('Looking for author named ' + authorName)
#             Author.objects.get(name=authorName)
#             print('Author exists')
#         except Author.DoesNotExist:
#             print('Author named ' + authorName + ' does not exist')
#             newAuthor = Author(name=authorName)
#             newAuthor.save()
#             print('added new author named ' + authorName)
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Book, Author
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def results(request):
    search_type = request.POST['search-type']
    query = request.POST['search']
    books = []


    #TODO: Find an efficient way to filter results based on user input
    if search_type == "author":
        try:
            #author = Author.objects.get(author_last_name__iexact=query)
            #books = Book.objects.filter(author=author)
            books = Book.objects.filter(author__author_last_name__icontains=query)
        except:
            pass
    else: #search_type == "title":
        books = Book.objects.filter(book_title=query)

    context = {"books": books, "query": query, "form_submitted": request.POST}
    return render(request, 'library/search.html', context)


def search(request):
    context = {"form_submitted": request.POST}
    try:
        search_type = request.POST['search-type']
        query = request.POST['search']
    except KeyError:
        # Nothing was entered so go to default search page
        return render(request, 'library/search.html', context)
    else:
        # Something was entered so go to results page
        # TODO: Make it save search type after redirect??
        return HttpResponseRedirect(reverse('library:results'))


def book_request(request, book_id):
    # TODO: Create feature so books may be placed on hold
    book = get_object_or_404(Book, pk=book_id)
    context = {"book": book }
    return render(request, 'library/request.html', context)


def checkout(request):
    context = dict()
    try:
        u = User.objects.get(pk=request.POST['user_id'])
        book = Book.objects.get(pk=request.POST['book_id'])
    except:
        return render(request, 'library/checkout.html', context)
    else:
        book.books_checked_out += 1
        book.save()
        msg = "Successfully checked out " + book.book_title
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect(reverse('library:checkout'))



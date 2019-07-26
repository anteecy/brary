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
            books = Book.objects.filter(book_author__author_last_name__icontains=query)
        except:
            pass
    else: #search_type == "title":
        books = Book.objects.filter(book_title__icontains=query)

    context = {"books": books, "query": query, "form_submitted": request.POST}
    return render(request, 'library/search.html', context)


def search(request):
    context = {"form_submitted": request.POST}
    try:
        search_type = request.POST['search-type']
        query = request.POST['search']
    except:
        # Nothing was entered so go to default search page
        return render(request, 'library/search.html', context)
    else:
        # Something was entered so go to results page
        return HttpResponseRedirect(reverse('library:results'))

def book_request(request, book_id):
    # TODO: Create feature so books may be placed on hold

    # Do book renewals first???

    book = get_object_or_404(Book, pk=book_id)
    context = {"book": book }
    return render(request, 'library/request.html', context)


def checkout(request):
    # TODO: BARCODE SCANNER
    context = dict()
    try:
        u = User.objects.get(pk=request.POST['user_id'])
        book = Book.objects.get(pk=request.POST['book_id'])

    except (User.DoesNotExist, Book.DoesNotExist, ValueError) as e:
        context['error_msg'] = "Invalid user or book ID"
        return render(request, 'library/checkout.html', context)
    except:
        # Show regular page
        return render(request, 'library/checkout.html', context)

    else:
        # Only if the book is available can it be checked out ...
        if book.book_available == True:
            book.book_available = False
            book.book_owner = u
            book.save()
            msg = "Successfully checked out " + book.book_title
            msg += " for " + u.username
            messages.add_message(request, messages.SUCCESS, msg)
        else:
        # Book was not available
            msg = "Book is already checked out by " + book.book_owner.username
            messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse('library:checkout'))

def returns(request):
    context = dict()
    try:
        book = Book.objects.get(pk=request.POST['book_id'])
        u = User.objects.get(pk=book.book_owner.id)

    except Book.DoesNotExist:
        context['error_msg'] = "Invalid book ID"
        return render(request, 'library/returns.html', context)
    except ValueError:
        # Must enter a book id 
        context['error_msg'] = "Book ID must be a number"
        return render(request, 'library/returns.html', context)
    except AttributeError:
        # Book has not been checked out and cannot be returned
        context['error_msg'] = "Book was never checked out"
        return render(request, 'library/returns.html', context)
    except:
        # Show regular page
        return render(request, 'library/returns.html', context)

    else:
        msg = u.username + " returned " + book.book_title
        messages.add_message(request, messages.SUCCESS, msg)
        book.book_available = True
        book.book_owner = None
        book.save()
        return HttpResponseRedirect(reverse('library:returns'))



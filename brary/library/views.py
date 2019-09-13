from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Book, Author
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta

def librarian_check(user):
    """
    Checks to see if user is a librarian
    """
    return user.groups.filter(name='librarian').exists()


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

@login_required
def book_request(request, book_id):

    book = get_object_or_404(Book, pk=book_id)
    context = {"book": book }

    if request.POST:
        # User wants to request a book
        context['requested'] = True
        book.book_requester = request.user
        book.book_available = False
        book.book_due_date = datetime.now() + timedelta(weeks=1)
        book.save()
    else:
        context['requested'] = False

    return render(request, 'library/request.html', context)

@user_passes_test(librarian_check)
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
        if book.book_available == True or book.book_requester == u:
            book.book_available = False
            book.book_owner = u
            book.book_requester = None
            book.book_due_date = datetime.now() + timedelta(weeks=3)
            book.save()
            msg = "Successfully checked out " + book.book_title
            msg += " for " + u.username
            msg += ". It is due on " + book.book_due_date.strftime("%a %B %-m") 
            msg += " at " + book.book_due_date.strftime("%-I %p")
            messages.add_message(request, messages.SUCCESS, msg)
        else:
        # Book was not available
            msg = str(book) + " is not available currently, however; you may request it!"
            messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse('library:checkout'))


@user_passes_test(librarian_check)
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


@user_passes_test(librarian_check)
def renew(request):
    context = dict()
    try:
        book = Book.objects.get(pk=request.POST['book_id'])
        u = User.objects.get(pk=book.book_owner.id)
    except ValueError:
        # Must enter a book id 
        context['error_msg'] = "Book ID must be a number"
        return render(request, 'library/renew.html', context)
    except AttributeError:
        # Book has not been checked out and cannot be returned
        context['error_msg'] = "Book was never checked out"
        return render(request, 'library/renew.html', context)
    except:
        return render(request, 'library/renew.html', context)

    else:

        if book.book_requester:
            # There is someone who has placed a request on the book so it cant
            # be renewed ...
            msg = book.book_title + " is on hold, and it " 
            msg += "cannot be renewed."
            messages.add_message(request, messages.ERROR, msg)
        else:
            # The book may be renewed
            book.book_due_date = datetime.now() + timedelta(weeks=3)
            book.save()
            msg = u.username + " renewed " + book.book_title + ". "
            msg += "it is now due on " + book.book_due_date.strftime("%a %B %-m")
            msg += " at " + book.book_due_date.strftime("%-I %p")
            messages.add_message(request, messages.SUCCESS, msg)

        return HttpResponseRedirect(reverse('library:renew'))

@login_required
def my_books(request):
    context = dict()
    books = Book.objects.filter(book_owner=request.user)
    holds = Book.objects.filter(book_requester=request.user)
    context['books'] = books
    context['holds'] = holds
    return render(request, 'library/my_books.html', context)


def user_hold_cancel(request):
    return HttpResonse("hello")

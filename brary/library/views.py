from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Book

# Create your views here.

def results(request):
    search_type = request.POST['search-type']
    query = request.POST['search']

    books = Book.objects.filter(book_title=query)
    context = {"books": books, "query": query}
    return render(request, 'library/results.html', context)


def search(request):
    context = dict()
    try:
        search_type = request.POST['search-type']
        query = request.POST['search']
    except KeyError:
        return render(request, 'library/search.html', context)
    else:
        return HttpResponseRedirect(reverse('library:results'))


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Book, Author

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

    context = {"books": books, "query": query}
    return render(request, 'library/results.html', context)


def search(request):
    context = dict()
    try:
        search_type = request.POST['search-type']
        query = request.POST['search']
    except KeyError:
        # Nothing was entered so go to default search page
        return render(request, 'library/search.html', context)
    else:
        # Something was entered so go to results page
        #TODO: Make this all in the search page??
        return HttpResponseRedirect(reverse('library:results'))


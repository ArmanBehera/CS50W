from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from . import util

class SearchForm(forms.Form):
    search=forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : SearchForm()
    })

def renderFile(request, filename):
    files = util.list_entries()

    if filename not in files:
        return render(request, "encyclopedia/error.html", {
            "form" : SearchForm()
        })
    else:
        return render(request, "encyclopedia/file.html", {
            "filename" : filename,
            "file" : util.get_entry(filename.capitalize()),
            "form" : SearchForm() 
        })

def wiki(request):
    searchResult = SearchForm(request.POST)
    
    print()
    print()
    print(searchResult)

    if searchResult.is_valid():
        search = searchResult.cleaned_data["search"]
        return HttpResponseRedirect(reverse(f"renderFile filename={search}"))
    else:
        return HttpResponse("Failure")
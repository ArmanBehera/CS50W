from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from markdown2 import Markdown

from . import util

markdowner = Markdown()


class SearchForm(forms.Form):
    """
        Creates a search field that is used in layout.html
    """
    search = forms.CharField()


def index(request):
    """
        Homepage/Root route for the wikipedia. Renders index.html
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : SearchForm()
    })


# Buggy. to be fixed
def wiki(request):
    """
        Only used for search button.
         Redirects to 'renderFile' url when the search button is clicked.
    """
    searchResult = SearchForm(request.POST)

    if searchResult.is_valid():
        search = searchResult.cleaned_data["search"]
        return HttpResponseRedirect(reverse("renderFile", kwargs={"filename" : search}))
    else:
        return HttpResponse("Failure")


def renderFile(request, filename):
    """
    Renders file in markdown format to HTML format.
    """

    file = util.get_entry(filename)

    if file is None:
        return render(request, "encyclopedia/error.html", {
            "form" : SearchForm()
        })
    else:
        return render(request, "encyclopedia/file.html", {
            "filename" : filename,
            "file" : markdowner.convert(file)
        })
    
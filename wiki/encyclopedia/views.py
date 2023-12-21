from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from markdown2 import Markdown
import random

from . import util

markdowner = Markdown()


class SearchForm(forms.Form):
    """
        Creates a search field that is used in layout.html
    """
    search = forms.CharField()

class NewPageTextArea(forms.Form):
    """
        Creates a text area to create new text files.
    """

    title = forms.CharField()
    textArea = forms.CharField(widget=forms.Textarea(attrs={'cols' : 120, 'rows': 20}), label="")


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
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/file.html", {
            "filename" : filename,
            "file" : markdowner.convert(file)
        })

def newPage(request):
    """
        Creates a new page and when submitted stores it locally.
    """

    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "textAreaForm" : NewPageTextArea()
        })
    else:

        formResult = NewPageTextArea(request.POST)

        if formResult.is_valid():
            titleResult = formResult.cleaned_data["title"]
            textAreaResult = formResult.cleaned_data["textArea"]

            util.save_entry(titleResult, textAreaResult)

        return HttpResponseRedirect(reverse("index"))


def editIndex(request):

    return render(request, "encyclopedia/editIndex.html", {
        "entries" : util.list_entries()
    })


def edit(request, filename):
    
    if request.method == "GET":
        file = util.get_entry(filename)

        if file is None:
            return render(request, "encyclopedia/error.html")
        else:
            initial_data = {
                'title' : filename,
                'textArea' : file
            }



            return render(request, "encyclopedia/edit.html", {
                "filename" : filename,
                "textAreaForm" : NewPageTextArea(initial=initial_data)
            })
    else:

        result = NewPageTextArea(request.POST)

        if result.is_valid():

            editResult = result.cleaned_data["textArea"]
            util.save_entry(filename, editResult)

        return HttpResponseRedirect(reverse("index"))

def randomPage(request):

    """
        Redirects the user to a random page
    """

    all_entries = util.list_entries()

    randomNum = random.randint(0, (len(all_entries) - 1))

    return HttpResponseRedirect(reverse("renderFile", kwargs={"filename" : all_entries[randomNum]}))
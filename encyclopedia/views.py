from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from markdown2 import Markdown
markdowner = Markdown()

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def contents(request,title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request,"encyclopedia/error.html",{"message": f"requested page ({title}) was not found."})
    return render(request, "encyclopedia/contents.html",{ "content": markdowner.convert(entry),"title":title})

def search(request):
    title = [request.GET["q"]]
    entries = []
    for entry in util.list_entries():
        entries.append(entry.lower())
    if title[0].lower() not in entries:
        searchRes=[]
        for entry in entries:
            if title[0].lower() in entry:
                searchRes.append(entry.capitalize())
        return render(request,"encyclopedia/search.html",{"entries": searchRes})
    return HttpResponseRedirect(reverse("contents", args=(title)))

def isEntry(title):
    entries = []
    for entry in util.list_entries():
        entries.append(entry.lower())
    if title.lower() in entries:
        return True
    else:
        return False

def creatNewPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/creatNewPage.html")
    title = request.POST["title"]
    content = request.POST["content"]
    if isEntry(title):
        return render(request,"encyclopedia/error.html",{"message": f"page ({title}) is already exist."})
    util.save_entry(title, content)
    return render(request, "encyclopedia/contents.html",{ "content": markdowner.convert(content),"title":title})
    
def editContents(request,title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/editContents.html", {"content":markdowner.convert(content), "title":title})
    content = request.POST["content"]
    util.save_entry(title, content)
    return render(request, "encyclopedia/contents.html",{ "content": markdowner.convert(content),"title":title})

def randomPage(request):
    entries = util.list_entries()
    item = random.choice(entries)
    content = util.get_entry(item)
    return render(request, "encyclopedia/contents.html",{ "content": markdowner.convert(content),"title":item})
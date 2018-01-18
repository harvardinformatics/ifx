from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from ifx import settings


def index(request):
    context = {}
    template = loader.get_template("portal/index.html")
    return HttpResponse(template.render(context, request))


def odyssey(request):
    return render(request, "portal/odyssey.html",{ "settings" : settings})

def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split("/")[-1]
    template = loader.get_template("portal/" + load_template)
    return HttpResponse(template.render(context, request))


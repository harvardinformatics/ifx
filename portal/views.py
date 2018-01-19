from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from portal.models import Notice
from portal.forms import NoticeForm
from ifx import settings


def index(request):
    context = {}
    template = loader.get_template("portal/index.html")
    return HttpResponse(template.render(context, request))


# @login_required(login_url="/login")
def odyssey(request):
    return render(request, "portal/odyssey.html", {"settings" : settings})


# @login_required(login_url="/login")
def notices(request):
    """
    List Notices
    """
    context = {}
    try:
        notices = Notice.objects.all().order_by("-updated")
        context["notices"] = notices
    except Exception as e:
        context["error_message"] = "There was a system error retrieving the list of notices: %s" % str(e)
    
    return render(request, "portal/notices.html", context)


# @login_required(login_url="/login")
def edit_notice(request, pk=None):
    """
    Create or edit a Notice
    """
    if pk is None:
        form = NoticeForm()
        return render(request, "portal/edit_notice.html", {"form" : form})


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split("/")[-1]
    template = loader.get_template("portal/example/" + load_template)
    return HttpResponse(template.render(context, request))

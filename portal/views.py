from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from portal.models import Notice
from portal.forms import NoticeForm
from ifx import settings
import logging


logger = logging.getLogger(__name__)


def index(request):
    notices = Notice.objects.all().order_by("-updated")[:10]
    return render(request, "portal/index.html", {"notices" : notices})


# @login_required(login_url="/login")
def odyssey(request):
    return render(request, "portal/odyssey.html", {"settings" : settings})


def odyssey_migration(request):
    return render(request, "portal/odyssey_migration.html")


# @login_required(login_url="/login")
def notices(request, pk=None):
    """
    List Notices
    """
    context = {}
    try:
        if pk is None:
            notices = Notice.objects.all().order_by("-updated")
        else:
            try: 
                notices = Notice.objects.filter(id=int(pk))
            except Notice.DoesNotExist:
                raise Http404("Notice %s cannot be found" % str(pk))
        context["notices"] = notices
    except Exception as e:
        context["error_message"] = "There was a system error retrieving the list of notices: %s" % str(e)
    
    return render(request, "portal/notices.html", context)


# @login_required(login_url="/login")
def edit_notice(request, pk=None):
    """
    Create or edit a Notice
    """
    logger.debug("Editing notice with id %s" % str(pk))
    try:
        if request.POST:
            # Create a new one
            if pk is None:
                form = NoticeForm(request.POST)
            # Update existing
            else:
                try:
                    notice = Notice.objects.get(id=int(pk))
                    form = NoticeForm(request.POST, instance=notice)
                except Notice.DoesNotExist:
                    raise Http404("Notice %s cannot be found" % str(pk))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('notices'))
            else:
                return render(request, "portal/edit_notice.html", {"form" : form})
        else:
            # Display new form
            if pk is None:
                form = NoticeForm(initial={"author" : request.user})
            # Display existing Notice for edit
            else:
                try:
                    notice = Notice.objects.get(id=int(pk))
                    form = NoticeForm(instance=notice)
                except Notice.DoesNotExist:
                    raise Http404("Notice %s cannot be found" % str(pk))
                    logger.error("Notice %s cannot be found" % str(pk))

            return render(request, "portal/edit_notice.html", {"form" : form})

    except Exception as e:
        logger.exception("Error retrieving Notice %s" % str(pk))
        return render(request, "portal/edit_notice.html", {"error_message" : "Error retrieving Notice %s: %s" % (str(pk), str(e))})


def delete_notice(request, pk):
    try:
        if request.POST:
            Notice.objects.get(pk=pk).delete()
            return HttpResponseRedirect(reverse('notices'))
        else:
            try:
                notice = Notice.objects.get(pk=pk)
                return render(request, "portal/delete_notice.html", {"notice" : notice})
            except Notice.DoesNotExist:
                raise Http404("Notice %s cannot be found" % str(pk))
    except Exception as e:
        logger.exception("Error deleting Notice %s" % str(pk))
        return render(request, "portal/delete_notice.html", {"error_message" : "Error deleting Notice %s: %s" % (str(pk), str(e))})


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split("/")[-1]
    template = loader.get_template("portal/example/" + load_template)
    return HttpResponse(template.render(context, request))

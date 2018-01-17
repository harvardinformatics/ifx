from django.conf.urls import url
from django.contrib.flatpages import views as v
from portal import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    url(r'^$', views.index, name='index'),
    url('<path:url>', v.flatpage),
]
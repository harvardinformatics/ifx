from django.conf.urls import url
from django.contrib.flatpages import views as v
from portal import views
from portal.admin import admin_site as admin

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^odyssey/migration/', views.odyssey_migration, name="odyssey_migration"),
    url(r'^odyssey/', views.odyssey, name="odyssey"),
    url(r'^notices/new/', views.edit_notice, name="new_notice"),
    url(r'^notices/edit/(?P<pk>\d+)/', views.edit_notice, name="edit_notice"),
    url(r'^notices/delete/(?P<pk>\d+)/', views.delete_notice, name="delete_notice"),
    url(r'^notices/(?P<pk>\d+)/', views.notices, name="view_notice"),
    url(r'^notices/$', views.notices, name="notices"),
    url(r'^example.*\.html', views.gentella_html, name="gentella"),

    # The home page
    url(r'^$', views.index, name="index"),
    url(r'^index.html$', views.index, name="index"),
    url("<path:url>", v.flatpage),
]

from __future__ import unicode_literals

from django.db import models


class Notice(models.Model):
    '''
    Meta data for an access to resources or actions or services.  Used to help setup the web page listing existing grants 
    and those that you can ask for.
    '''
    class Meta:
        db_table = "notice"

    content             = models.TextField(blank=False, null=False, help_text="Notice text, using Markdown.")
    author              = models.CharField(max_length=100, blank=False, null=False, help_text="Author of the Notice")
    created             = models.DateField(auto_now_add=True, help_text="When the Notice was created.")
    updated             = models.DateField(auto_now=True, help_text="Last update date")

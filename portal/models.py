from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model


class Notice(models.Model):
    """
    Meta data for an access to resources or actions or services.  Used to help setup the web page listing existing grants
    and those that you can ask for.
    """
    class Meta:
        db_table = "notice"

    title               = models.CharField(blank=False, null=False, max_length=100, help_text="Title for the notice")
    content             = models.TextField(blank=False, null=False, help_text="Notice text, using Markdown.")
    excerpt             = models.CharField(blank=True, null=True, max_length=400, help_text="An excerpt to be used for the front page.")
    author              = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, blank=True, null=False, help_text="Author of the article")
    created             = models.DateTimeField(auto_now_add=True, help_text="When the Notice was created.")
    updated             = models.DateTimeField(auto_now=True, help_text="Last update date")


class Account(models.Model):
    """
    Model for accounts linked to the user.  Probably will just be RC
    """
    class Meta:
        db_table = "account"

    name                = models.CharField(blank=False, null=False, max_length=100, help_text="Name of the account")
    identifier          = models.CharField(blank=False, null=False, max_length=100, help_text="User identifier used for thsi account")
    user                = models.ForeignKey(get_user_model(), blank=False, null=False, on_delete=models.CASCADE, help_text="User associated with this account.")

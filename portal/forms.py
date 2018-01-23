"""
forms for Portal applications
"""
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
from portal.models import Notice


class UserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.first_name.strip() != "":
            return "%s %s" % (obj.first_name, obj.last_name)
        else:
            return obj.username


class NoticeForm(forms.ModelForm):
    """
    Notice Form
    """
    class Meta:
        model = Notice
        fields = ["title", "content", "author", "excerpt"]

    title       = forms.CharField(widget=forms.TextInput(attrs={'size' : 50}), required=True, help_text="Title for the Notice.")
    content     = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows"          : 10, 
                "class"         : "resizable_textarea form-control",
                "placeholder"   : "Use Markdown for styling",
            }
        ), 
        required=True)
    excerpt     = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows"          : 10, 
                "class"         : "resizable_textarea form-control",
                "placeholder"   : "Excerpt for the front page, if the notice is long.  Markdown works here.",
            }
        ), 
        required=True)
    author      = UserChoiceField(queryset=User.objects.all(), required=True, empty_label=None)

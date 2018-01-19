"""
forms for Portal applications
"""
from django import forms


class NoticeForm(forms.Form):
    """
    Notice Form
    """
    content     = forms.CharField(widget=forms.Textarea(attrs={"rows" : 18, "cols" : 60, "title" : "Notice content, Markdown acceptable."}), required=True)
    author      = forms.CharField(widget=forms.TextInput(attrs={"size" : 30, "title" : "User name of the Notice author"}), required=True)

from django import forms
from .models import Forum


# Region form
class CreateForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['name', 'description', 'region']

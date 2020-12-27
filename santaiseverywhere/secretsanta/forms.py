from django import forms
from django.forms import widgets
from taggit.managers import TaggableManager
from taggit.forms import TagField

from .models import Room 

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name','description','budget','password','masterPassword')
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder':'normal authentication password'}),
            'masterPassword': forms.PasswordInput(attrs={'placeholder':'master password'}),
        }


class SendInvitation(forms.Form):
    to = TagField(widget=forms.TextInput(attrs={'placeholder':'Enter to emails seperated by a ","'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Master Password'}))
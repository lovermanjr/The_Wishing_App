"""
Definition of forms.
"""

from django import forms
from django.forms import HiddenInput
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import User, Wish

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class WishForm(forms.ModelForm):
    class Meta:
        model = Wish
        fields = 'title', 'description'
        labels = {
            'title' : 'I wish for:'
            }
        #fields = '__all__'
        #widgets = {'user': HiddenInput()}

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

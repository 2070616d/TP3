# -*- coding: iso-8859-1 -*-
from django import forms
from django.contrib.auth.models import User
from stove.models import *


class UserForm(forms.ModelForm):
    """Form that creates a User object."""

    password2 = forms.CharField(widget=forms.PasswordInput())
    tandc = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # add custom error messages
        self.fields['username'].error_messages = {'required': 'Please enter a username.'}
        self.fields['email'].error_messages = {'required': 'Please enter an email address.'}
        self.fields['password'].error_messages = {'required': 'Please enter a password.'}
        self.fields['password2'].error_messages = {'required': 'Please confirm your password.'}
        self.fields['tandc'].error_messages = {'required': 'Please agree to our terms & conditions.'}
        self.fields['first_name'].error_messages = {'required': 'Please enter your first name.'}
        self.fields['last_name'].error_messages = {'required': 'Please enter your last name.'}

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if cleaned_data.get("password") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords don't match!")


class UserProfileFormRegister(forms.ModelForm):
    """
    Form that creates a UserProfile object.
    Used for sign-up.
    """

    def __init__(self, *args, **kwargs):
        super(UserProfileFormRegister, self).__init__(*args, **kwargs)

        # add custom error messages
        self.fields['postcode'].error_messages = {'required': 'Please enter your postcode.'}
        self.fields['dateOfBirth'].error_messages = {'required': 'Please enter your date of birth.'}

    class Meta:
        model = UserProfile
        fields = ('postcode', 'dateOfBirth', 'gender')


class UserProfileForm(forms.ModelForm):
    """
    Form that modifies a UserProfile object.
    Used for the edit profile page.
    """

    class Meta:
        model = UserProfile
        fields = ('postcode', 'dateOfBirth', 'gender', 'avatar')


class LoginForm(forms.Form):
    """Form that logs (non-social login) users in."""

    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput())
    remember = forms.BooleanField(required=False, widget=forms.CheckboxInput())


class PrefCheckbox(forms.Form):
    """Individual preference checkboxes are their own forms, due to the Django formset paradigm."""

    checked = forms.BooleanField()


class EventCheckbox(forms.Form):
    """Individual event attendance checkboxes are their own forms, due to the Django formset paradigm."""

    checked = forms.BooleanField()


class EventDropdown(forms.Form):
    """
    Event choice drop-down menu.
    Used in the event profiler tool.
    """

    events = forms.ModelChoiceField(queryset=Event.objects.all())

    class Meta:
        model = Event
        exclude = ['picture']

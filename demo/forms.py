from django import forms
from django.forms import Form, CharField, BooleanField, Textarea
from django.forms import TextInput, PasswordInput, CheckboxInput
from django.forms import HiddenInput

class EditObjectForm(Form):
    # Object name
    attrs = {'readonly': 'readonly'}
    object_name = CharField(widget=TextInput(attrs=attrs))

    # Data
    attrs = {'autofocus': 'autofocus', 'required': 'true'}
    data = CharField(widget=Textarea(attrs=attrs))

class CreateObjectForm(Form):
    # Object name
    attrs = {'autofocus': 'autofocus', 'required': 'true'}
    object_name = CharField(widget=TextInput(attrs=attrs))

    # Data
    attrs = {'required': 'true'}
    data = CharField(widget=Textarea(attrs=attrs))

class LoginForm(Form):
    # User name
    attrs = {'autofocus': 'autofocus', 'required': 'true'}
    username = CharField(widget=TextInput(attrs=attrs))

    attrs = {'required': 'true'}
    password = CharField(widget=PasswordInput(attrs=attrs))

    remember_me = BooleanField(required=False, initial=True)
    
    next_url = CharField(widget=HiddenInput())


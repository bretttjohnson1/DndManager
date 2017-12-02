from django import forms
from django.forms import ModelForm
from website.models import *

class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirm Password", max_length=100, widget=forms.PasswordInput())


class SessionForm(forms.Form):
    session_key = forms.HiddenInput()

class CharacterModelForm(ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'game_id', 'race', 'classname', 'level']


class BaseStatsModelForm(ModelForm):
    class Meta:
        model = Base_Stats
        fields = ['str', 'con', 'dex', 'int', 'wis','cha']

class FormData():
    def __init__(self, formname, formurl):
        self.formname = formname
        self.formurl = formurl


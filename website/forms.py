from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirm Password", max_length=100, widget=forms.PasswordInput())


class SessionForm(forms.Form):
    session_key = forms.HiddenInput()



from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=100)
    password = forms.CharField(label="Password", max_length=100)


class RegisterForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=100)
    password = forms.CharField(label="Password", max_length=100)
    confirm_password = forms.CharField(label="Confirm Password", max_length=100)
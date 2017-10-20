from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)

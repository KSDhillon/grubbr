from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)

class CreateMealForm(forms.Form):
    name = forms.CharField(label='Name', max_length=200)
    price = forms.IntegerField(label='Price', min_value=0)
    description = forms.CharField(label='Description', max_length=500)
    portions = forms.IntegerField(label='Portions', min_value=1)

class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=200)

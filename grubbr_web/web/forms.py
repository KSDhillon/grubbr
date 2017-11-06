from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, label="")
    email.widget.attrs.update({'placeholder' : 'Email', 'class': 'form-control form-control-lg'})
    password = forms.CharField(widget=forms.PasswordInput(), label="")
    password.widget.attrs.update({'placeholder' : 'Password', 'class': 'form-control form-control-lg'})

class RegisterForm(forms.Form):
    email = forms.EmailField(label='', max_length=100)
    email.widget.attrs.update({'placeholder' : 'Email', 'class': 'form-control form-control-lg'})
    password = forms.CharField(label='', widget=forms.PasswordInput())
    password.widget.attrs.update({'placeholder' : 'Password', 'class': 'form-control form-control-lg'})
    first_name = forms.CharField(label='', max_length=100)
    first_name.widget.attrs.update({'placeholder' : 'First Name', 'class': 'form-control form-control-lg'})
    last_name = forms.CharField(label='', max_length=100)
    last_name.widget.attrs.update({'placeholder' : 'Last Name', 'class': 'form-control form-control-lg'})

class CreateMealForm(forms.Form):
    name = forms.CharField(label='', max_length=200)
    price = forms.IntegerField(label='', min_value=0)
    description = forms.CharField(label='', max_length=500)
    portions = forms.IntegerField(label='', min_value=1)

    name.widget.attrs.update({'placeholder' : 'Name', 'class': 'form-control form-control-lg'})
    price.widget.attrs.update({'placeholder' : 'Price', 'class': 'form-control form-control-lg'})
    description.widget.attrs.update({'placeholder' : 'Description', 'class': 'form-control form-control-lg'})
    portions.widget.attrs.update({'placeholder' : 'Portions', 'class': 'form-control form-control-lg'})
class SearchForm(forms.Form):
    q = forms.CharField(label='', max_length=200)
    q.widget.attrs.update({'placeholder' : 'Search', 'class': 'form-control'})

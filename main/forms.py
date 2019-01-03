from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)

class MessageForm(forms.Form):
    message = forms.CharField(label='textarea', max_length=500, required=True)
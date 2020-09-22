from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='')
    last_name = forms.CharField(max_length=30, required=False, help_text='')
    email = forms.EmailField(max_length=254, help_text='Provide a valid email address.')
    account_type = forms.ChoiceField(choices=(('', '---------'),('player','Player'),('developer','Developer')), required=True) #widget=forms.Select()
    avatar = forms.ImageField(required=False, help_text='Upload an avatar picture') #requires Pillow to be installed (pip install Pillow)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'account_type', 'avatar')

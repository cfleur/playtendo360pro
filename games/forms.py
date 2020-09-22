from django import forms
from django.forms import ModelForm
from games.models import Game


class SubmitForm(ModelForm):
    price = forms.FloatField(help_text='Insert 0 for free games. Maximum is 100', min_value=0, max_value=100)
    link = forms.URLField(label='Link to the game', help_text='Provide an URL to an HTML file of the game')
    preview_pic = forms.ImageField(label='Preview image', required=False, help_text='Provide an image which will be displayed as a preview for the game') #requires Pillow to be installed (pip install Pillow)
    class Meta:
        model = Game
        fields = ['title', 'description', 'link', 'genre', 'price', 'preview_pic']

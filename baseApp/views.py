from django.shortcuts import render
from games.models import Game
from django.forms.models import model_to_dict
from django.views.generic import ListView


class GameListHome(ListView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameListHome, self).get_context_data(**kwargs)
        if Game.objects.all().exists():
            context['games'] = Game.objects.all()
        return context


    # context_object_name = 'game'



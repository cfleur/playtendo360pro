from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import DetailView
from games.forms import SubmitForm
from games.models import Game, Score
from authentication.models import Account
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class GameDetail(DetailView):
    contex_object_name = 'game'
    model = Game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['User'] = Account.objects.get(id=self.request.user.id) # get Account object

            # check if game is owned by user
            context['game_is_owned'] = False
            owned_games = Account.objects.get(id=self.request.user.id) # TODO: implement proper query for this
            if not owned_games: # change to positive condition to check it works
                context['game_is_owned'] = True

            # context['fake_account_type'] = 'developer' # For testing TODO: remember to remove condition form template
            context['fake_account_type'] = 'player' # For testing TODO: remember to remove condition form template

            # leaderboard List
        context['leaderboard'] = Score.objects.filter(game=Game.objects.get(pk=self.kwargs['pk'])).order_by('-score')[:10]
        return context

    def dispatch(self, request, *args, **kwargs):
        pk = get_object_or_404(Game, pk=self.kwargs['pk']).pk # throw 404 if the game does not exist
        if self.request.user.is_authenticated:
            user = Account.objects.get(id=self.request.user.id)
        try:
            user.owned_games.get(pk=pk) # checks if the user owns the game
            return redirect (reverse('game-play', args=(pk,))) # redirects them to the pay page if they do
        except:
            return super(GameDetail, self).dispatch(request, *args, **kwargs) # return the detail view if they don't



class PlayGame(DetailView):
    contex_object_name = 'game'
    model = Game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'payment_success' in self.request.GET:
            print(self.request.GET['payment_success'])
            context['payment_success'] = self.request.GET['payment_success']
        context['leaderboard'] = Score.objects.filter(game=Game.objects.get(pk=self.kwargs['pk'])).order_by('-score')[:10]
        return context



    def dispatch(self, request, *args, **kwargs):
        user = Account.objects.get(id=self.request.user.id)
        game = get_object_or_404(Game, pk=self.kwargs['pk'])
        try: # checks if game is in the user's game list
            user.owned_games.get(pk=self.kwargs['pk'])
            # print(user.owned_games.all(), self.kwargs['pk'])
            #return(request, 'game-play', pk=game.pk)
        except:
            raise PermissionDenied
        if request.method == 'POST':
            try:
                p_score = Score.objects.get(game=game, player=user)

                if p_score.score < float(request.POST['score']):
                    print("request.POST['score'] = " + request.POST['score'])
                    print("p_score.score = " + str(p_score.score))
                    p_score.score = float(request.POST['score'])
                    print("p_score.score = " + str(p_score.score))
                    p_score.save()
                    print("p_score.score = " + str(p_score.score))

            except ObjectDoesNotExist:
                score = Score(score=request.POST['score'], player=user, game=game)
                score.save()

            except MultipleObjectsReturned:
                pass

            return HttpResponseRedirect(self.request.path_info)
        return super().dispatch(request, *args, **kwargs)




@login_required
def submit_game(request):
    cur_user = Account.objects.get(id=request.user.id)
    if cur_user.account_type=='player': #no permission if user is not a developer
        return render(request, 'unpermitted.html')
    else:
        if request.method == 'POST':
            form = SubmitForm(request.POST, request.FILES)
            if form.is_valid():
                #insert the new game into db
                game=Game(title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
                genre=form.cleaned_data.get('genre'),
                link=form.cleaned_data.get('link'),
                developer=cur_user)
                #check if preview pic was submitted and if so, add it to the game
                if form.cleaned_data['preview_pic'] is not None:
                    game.preview_pic = form.cleaned_data['preview_pic']
                game.save()
                #make dev also an owner
                game.owners.add(cur_user)
                return HttpResponseRedirect('/accounts/profile/')
        else:
            form = SubmitForm()

        return render(request, 'submit.html', {'form': form})

@login_required
def modify_game(request, pk):
    cur_user = Account.objects.get(id=request.user.id)
    game = Game.objects.get(pk=pk)
    if game.developer.id == cur_user.id: #checking if the user is the developer
        if request.method == 'POST':
            game.description = request.POST['descrip']
            game.genre = request.POST['genre']
            game.price = request.POST['price']
            if request.FILES.get('pic') is not None:
                game.preview_pic = request.FILES['pic']
            game.save()

            '''possible TODO game deletion'''

        return render(request, 'modify.html', {'game': game})
    else:
         return render(request, 'unpermitted.html') #no permission if user is not THE developer

'''
@login_required
def update_score(request, pk):
    user = Account.objects.get(id=request.user.id)
    game = Game.objects.get(pk=pk)
    if request.method == 'POST':
        #check if score higher
        score = Score(score=request.POST['score'],player=user, game=game)
        score.save()
    return render(request, 'game_detail.html', {'game': game, 'user': user})
'''

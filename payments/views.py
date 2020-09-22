from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.forms.models import model_to_dict
from hashlib import md5
from decimal import *

from authentication.models import Account
from games.models import Game
from gamesite import settings



def calculate_md5(**kwargs):
    ''' Calculates the md5 checksums to validate payments'''
    kwargs['sid'] = settings.SECRETISH_SELLER_ID
    kwargs['secret_key'] = settings.VERY_SECRET_PAYMENTS_KEY
    if 'amount' in kwargs.keys():
        checksumstr = "pid={pid}&sid={sid}&amount={amount}&token={secret_key}".format(**kwargs)
    if 'ref' in kwargs.keys():
        checksumstr = "pid={pid}&ref={ref}&result={result}&token={secret_key}".format(**kwargs)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    return checksum


class PayForGame(DetailView):
    model = Game
    context_object_name = 'game'

    def dispatch(self, request, *args, **kwargs):
        pk = get_object_or_404(Game, pk=self.kwargs['pk']).pk  # throw 404 if the game does not exist
        if self.request.user.is_authenticated:
            user = Account.objects.get(id=self.request.user.id)
            if user.account_balance < Game.objects.get(pk=pk).price:
                return redirect('pay-error', pk=pk)
        try:
            user.owned_games.get(pk=pk)  # checks if the user owns the game
            return redirect(reverse('game-play', args=(pk,)))  # redirects them to the pay page if they do
        except:
            return super(PayForGame, self).dispatch(request, *args, **kwargs)
        # TODO: check that there is enough money in the user's account, implement the following:



    def get_context_data(self, **kwargs):
        context = super(PayForGame, self).get_context_data(**kwargs)
        buyer = Account.objects.get(id=self.request.user.id)
        purchase_game = get_object_or_404(Game, pk=self.kwargs['pk'])
        amount = Decimal(purchase_game.price)
        pid = '{}z{}'.format(purchase_game.id, buyer.id)
        context['pid'] = pid
        context['amount'] = amount
        host = settings.HOST
        context['cancel_url'] = '{}/games/{}'.format(host, purchase_game.id)
        context['error_url'] = '{}/pay/error/{}'.format(host, purchase_game.id)
        context['success_url'] = '{}/pay/success/{}'.format(host, purchase_game.id)
        checksum_obj = {}
        checksum_obj['pid'] = pid
        checksum_obj['amount'] = amount
        context['checksum'] = calculate_md5(**checksum_obj)
        return context




def payment_error(request, pk):
    ''' Handle error payment cases '''
    purchase_game = Game.objects.get(pk=pk)
    return render(request, 'pay_error.html', {'game' : purchase_game})




def payment_success(request, pk):
    ''' Handle the successfully returned payment from the service '''
    purchase_game = Game.objects.get(pk=pk)
    new_owner = Account.objects.get(id=request.user.id)
    query_params = request.GET
    our_pid = '{}z{}'.format(purchase_game.id, new_owner.id)
    try:
        purchase_game.owners.get(id=request.user.id)
        return redirect('game-play', pk=pk)
    except:
        pass
    # sent_purchase_id = query_params['pid'].split('z', 2)[0] # checks that this is the right game, maybe not necessary
    if 'pid' and 'ref' and 'result' and 'checksum' in query_params and query_params['pid'] == our_pid and query_params['result'] == "success":
    # if query_params['pid'] == our_pid and str(sent_purchase_id) == str(purchase_game.id): # probably redundant, I can't think right now
        # checks the the pid is for the correct purchase; TODO: test this.
        if calculate_md5(**query_params.dict()) == query_params['checksum']:
            # game can only be purchased if the checksum sent from the seller is validated
            purchase_game.owners.add(new_owner) # adds game to user's game list
            new_owner.account_balance -= purchase_game.price
            new_owner.save()
            purchase_game.developer.account_balance += purchase_game.price
            purchase_game.developer.save()
            # Note that here, amount that is debited is equal to the price of the game at TIME OF PURCHASE COMPLETION not initiation
            return redirect ("%s?payment_success=%s" % (reverse('game-play', args=(pk,)), query_params['pid']))
        else:
            return redirect('pay-error', pk=pk)
    else:
        return redirect ('pay-error', pk=pk)

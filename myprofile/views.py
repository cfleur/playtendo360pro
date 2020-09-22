from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from authentication.models import Account, User
from games.models import Game


@method_decorator(login_required, name='dispatch')
class ProfileView(ListView):
    model = Game
    template_name = "profile.html"
    context_object_name = "user_games"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['User'] = Account.objects.get(id=self.request.user.id)
        # try:
        if Account.objects.get(id=self.request.user.id).submitted_games.exists():
            context['submitted_games'] = Account.objects.get(id=self.request.user.id).submitted_games.all()
        # except:
        #     pass
        # try:
        if Account.objects.get(id=self.request.user.id).owned_games.exists():
            context['owned_games'] = Account.objects.get(id=self.request.user.id).owned_games.all()
        # except:
        #     pass
        return context



    # def get_queryset(self):
    #     user = Account.objects.get(user=self.request.user)
    #     if user.account_type=='developer':
    #         try:
    #             return user.submitted_games.all()
    #         except:
    #             pass
    #     else:
    #         try:
    #             return user.owned_games.all()
    #         except:
    #             pass

@login_required
def modify_profile(request):
    if request.method == 'POST' and 'avatar_change' in request.POST:
        request.user.account.avatar = request.FILES['new_avatar']
        request.user.account.save()
        form = PasswordChangeForm(request.user)
    elif request.method == 'POST' and 'password_change' in request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important apparently
            messages.success(request, 'Password changed successfully')
            return redirect('modify profile')
        else:
            messages.error(request, 'Something did not quite match')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'modify_account.html', {'form': form})

@login_required
def add_money(request):
    user = Account.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.account_balance += float(request.POST['muhney'])
        user.save()
    return render(request, 'muhney.html')

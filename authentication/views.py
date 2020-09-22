from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from authentication.forms import RegistrationForm
from authentication.models import Account

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            acc_type = form.cleaned_data.get('account_type')
            user = authenticate(username=username, password=password)
            acc = Account(user=user, account_type=acc_type, user_id=user.id, id=user.id)
            if form.cleaned_data['avatar'] is not None:
                acc.avatar = form.cleaned_data['avatar']
            acc.save()
            login(request, user)
            return HttpResponseRedirect('/accounts/profile/') #redirect path after login here
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def signout(request):
    logout(request)
    return HttpResponseRedirect('/') #redirect path after logout here

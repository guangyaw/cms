from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from accounts.models import Profile
import requests

# API 位址  https://api.hitbtc.com/
# sample code ： https://github.com/hitbtc-com/hitbtc-api/blob/master/example_rest.py


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# def home(request):
# #     my_profile = Profile.objects.get(user__username='guangyaw')
# #     session = requests.session()
# #     session.auth = (my_profile.api_key, my_profile.secret_no)
# #     b = session.get('https://api.hitbtc.com/api/2/trading/balance').json()
# #     mybalances = []
# #     for balances in b:
# #         if balances["available"] != '0':
# #             mybalances.append(balances)
# #
# #     return render(request, "accounts/accounts_home.html", {"balance": mybalances, "title": 'test balance'})

def home(request):
    return HttpResponse('account home')


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            tmp = login_form.cleaned_data
            user = authenticate(username=tmp['username'], password=tmp['password'])
            if user:
                login(request, user)
                return HttpResponse('login successfully')
            else:
                return HttpResponse('login failed')
        else:
            return HttpResponse('invalid login')

    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'accounts/login.html', {'form': login_form})

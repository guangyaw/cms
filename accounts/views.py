from django.shortcuts import render
import requests
from accounts.models import Profile


# API 位址  https://api.hitbtc.com/
def home(request):
    my_profile = Profile.objects.get(user__username='guangyaw')
    session = requests.session()
    session.auth = (my_profile.api_key, my_profile.secret_no)
    b = session.get('https://api.hitbtc.com/api/2/trading/balance').json()
    mybalances = []
    for balances in b:
        if balances["available"] != '0':
            mybalances.append(balances)

    return render(request, "accounts/accounts_home.html", {"balance": mybalances, "title": 'test balance'})


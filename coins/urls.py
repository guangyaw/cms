"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from coins.views import coin_home, ethbtc_sell, ethbtc_buy, order_check

urlpatterns = [
    path('', coin_home, name='coin_home'),
    path('sample_sell/', ethbtc_sell, name='ethbtc_sell'),
    path('sample_buy/', ethbtc_buy, name='ethbtc_buy'),
    path('order_check/', order_check, name='order_check'),
]

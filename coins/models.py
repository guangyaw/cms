from django.db import models
from django.utils import timezone

# trade record sample
# {
#     "id": 737257068,
#     "clientOrderId": "e770315f09b54594bd0da22c5d8c1418",
#     "orderId": 189615504366,
#     "symbol": "ETHBTC",
#     "side": "sell",
#     "quantity": "0.0553",
#     "price": "0.017694",
#     "fee": "0.000000978479",
#     "timestamp": "2019-12-24T19:24:24.437Z"
#   },


class TradeRecord(models.Model):
    clientOrderId = models.CharField(max_length=20, default='', blank=True)
    symbol = models.CharField(max_length=20, default='', blank=True)
    side = models.CharField(max_length=20, default='', blank=True)
    quantity = models.CharField(max_length=30, default='', blank=True)
    price = models.CharField(max_length=30, default='', blank=True)
    fee = models.CharField(max_length=30, default='', blank=True)
    now_status = models.CharField(max_length=30, default='default', blank=True)
    wait_counter = models.IntegerField(default='0', blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.symbol


class BestValues(models.Model):
    start_point = models.IntegerField(default='99', blank=True)
    symbol = models.CharField(max_length=20, default='', blank=True)
    best_price = models.CharField(max_length=30, default='', blank=True)
    best_bid = models.CharField(max_length=30, default='', blank=True)
    best_ask = models.CharField(max_length=30, default='', blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.symbol


class PreOrder(models.Model):
    symbol = models.CharField(max_length=20, default='', blank=True)
    stop_point = models.IntegerField(default='20', blank=True)
    base_amount = models.CharField(max_length=20, default='', blank=True)
    end_amount = models.CharField(max_length=20, default='', blank=True)
    status = models.CharField(max_length=20, default='', blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.symbol

from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from accounts.models import Profile
from coins.models import BestValues, PreOrder, TradeRecord
import uuid
import time
import requests
from decimal import *
from django_q.models import Schedule
import datetime
# from django.utils import timezone
# from django.utils.timezone import get_current_timezone


class Client(object):
    def __init__(self, url, public_key, secret):
        self.url = url + "/api/2"
        self.session = requests.session()
        self.session.auth = (public_key, secret)

    def get_symbol(self, symbol_code):
        """Get symbol."""
        return self.session.get("%s/public/symbol/%s" % (self.url, symbol_code)).json()

    def get_orderbook(self, symbol_code):
        """Get orderbook. """
        return self.session.get("%s/public/orderbook/%s" % (self.url, symbol_code)).json()

    def get_address(self, currency_code):
        """Get address for deposit."""
        return self.session.get("%s/account/crypto/address/%s" % (self.url, currency_code)).json()

    def get_account_balance(self):
        """Get main balance."""
        return self.session.get("%s/account/balance" % self.url).json()

    def get_trading_balance(self):
        """Get trading balance."""
        return self.session.get("%s/trading/balance" % self.url).json()

    # def transfer(self, currency_code, amount, to_exchange):
    #     return self.session.post("%s/account/transfer" % self.url, data={
    #             'currency': currency_code, 'amount': amount,
    #             'type': 'bankToExchange' if to_exchange else 'exchangeToBank'
    #         }).json()

    def new_order(self, client_order_id, symbol_code, side, quantity, price=None):
        """Place an order."""
        data = {'symbol': symbol_code, 'side': side, 'quantity': quantity}

        if price is not None:
            data['price'] = price

        return self.session.put("%s/order/%s" % (self.url, client_order_id), data=data).json()

    def get_order(self, client_order_id, wait=None):
        """Get order info."""
        data = {'wait': wait} if wait is not None else {}

        return self.session.get("%s/order/%s" % (self.url, client_order_id), params=data).json()

    def get_open_order(self):
        """Get all open order info."""
        return self.session.get("%s/order/" % (self.url,)).json()

    def cancel_order(self, client_order_id):
        """Cancel order."""
        return self.session.delete("%s/order/%s" % (self.url, client_order_id)).json()

    # def withdraw(self, currency_code, amount, address, network_fee=None):
    #     """Withdraw."""
    #     data = {'currency': currency_code, 'amount': amount, 'address': address}
    #
    #     if network_fee is not None:
    #         data['networkfee'] = network_fee
    #
    #     return self.session.post("%s/account/crypto/withdraw" % self.url, data=data).json()

    # def get_transaction(self, transaction_id):
    #     """Get transaction info."""
    #     return self.session.get("%s/account/transactions/%s" % (self.url, transaction_id)).json()


def check_open_and_auto_trade():
    print('check_open_and_auto_trade  ...')
    g_symbol = 'ETHBTC'

    my_profile = Profile.objects.get(user__username='guangyaw')
    client = Client("https://api.hitbtc.com", my_profile.api_key, my_profile.secret_no)
    open_orders = client.get_open_order()
    open_order_len = len(open_orders)
    if open_order_len == 0:
        #get last trade record
        # x = TradeRecord.objects.filter(Q(now_status= 'new')|Q(now_status= 'partiallyFilled'))
        # last_trade_id = ''
        # for target_items in x:
        #     last_trade_id = target_items.clientOrderId
        #     y = TradeRecord.objects.get(clientOrderId=last_trade_id)
        #     y.now_status = 'filled'
        #     y.save()
        #print(last_trade_id)
        eth_btc = client.get_symbol(g_symbol)
        # get trading balance
        eth_balance = 0.0
        btc_balance = 0.0
        balances = client.get_trading_balance()
        for balance in balances:
            if balance['currency'] == 'ETH':
                eth_balance = float(balance['available'])
            if balance['currency'] == 'BTC':
                btc_balance = float(balance['available'])

        orderbook = client.get_orderbook(g_symbol)
        order_avg = (Decimal(orderbook['bid'][0]['price']) + Decimal(orderbook['ask'][0]['price'])) / 2
        best_price = Decimal(order_avg)

        btc_balance_toETH = round(btc_balance / float(best_price), 4) - float(eth_btc['quantityIncrement'])
        print('check_open_and_auto_trade: BTC balance in ETH: %s ' % (btc_balance_toETH,))
        print('check_open_and_auto_trade: ETH balance: %s' % eth_balance)
        if TradeRecord.objects.filter(now_status='new').exists():
            print('debug point1')
            check_last = TradeRecord.objects.get(now_status='new')
            base_x = PreOrder.objects.get(status='running')
            target_rate = float(100 - base_x.stop_point)
            check_point = float(check_last.quantity) / float(base_x.base_amount) * 100
            print('check_open_and_auto_trade: amount rate: %s , target rate = %s ' % (check_point, target_rate))
            if check_point < target_rate:
                print('wait for user handle')
                return
            orderbook = client.get_orderbook(g_symbol)
            if eth_balance > btc_balance_toETH:
                # sell
                if eth_balance >= float(eth_btc['quantityIncrement']):
                    g_side = 'sell'
                    g_balance = eth_balance
                    client_order_id = uuid.uuid4().hex

                    order_avg = (Decimal(orderbook['bid'][0]['price']) + Decimal(orderbook['ask'][17]['price'])) / 2
                    best_price = Decimal(order_avg)

                    btc_balance_toETH = round(btc_balance / float(best_price), 4) - float(eth_btc['quantityIncrement'])
                    print("Selling at %s" % best_price)
            else:
                # buy
                if btc_balance_toETH >= float(eth_btc['quantityIncrement']):
                    order_avg = (Decimal(orderbook['bid'][2]['price']) + Decimal(orderbook['ask'][0]['price'])) / 2
                    best_price = Decimal(order_avg)

                    g_side = 'buy'
                    g_balance = btc_balance_toETH
                    client_order_id = uuid.uuid4().hex
                    print("buy at %s" % best_price)

            print(check_last.price)
            order = client.new_order(client_order_id, g_symbol, g_side, g_balance, best_price)
            if 'error' not in order:
                if order['status'] == 'filled':
                    print("Order filled", order)
                elif order['status'] == 'new' or order['status'] == 'partiallyFilled':
                    print("Waiting order...")

                TradeRecord.objects.create(clientOrderId=client_order_id, symbol=g_symbol, side=g_side,
                                           quantity=g_balance, price=best_price, now_status=order['status'])
            else:
                print(order['error'])
        else:#direct start
            print('debug point2')
            print('check_open_and_auto_trade: direct start')
            base_x = PreOrder.objects.get(status='running')
            target_rate = float(100 - base_x.stop_point)
            orderbook = client.get_orderbook(g_symbol)
            order_avg = (Decimal(orderbook['bid'][0]['price']) + Decimal(orderbook['ask'][0]['price'])) / 2
            best_price = Decimal(order_avg)
            btc_balance_toETH = round(btc_balance / float(best_price), 4) - float(eth_btc['quantityIncrement'])
            print("check_open_and_auto_trade: price at %s" % best_price)

            if eth_balance > btc_balance_toETH:
                # sell
                if eth_balance >= float(eth_btc['quantityIncrement']):
                    g_side = 'sell'
                    g_balance = eth_balance
                    client_order_id = uuid.uuid4().hex
                    order_avg = (Decimal(orderbook['bid'][0]['price']) + Decimal(orderbook['ask'][17]['price'])) / 2
                    best_price = Decimal(order_avg)
            else:
                # buy
                if btc_balance_toETH >= float(eth_btc['quantityIncrement']):
                    g_side = 'buy'
                    g_balance = btc_balance_toETH
                    client_order_id = uuid.uuid4().hex
                    print("buy at %s" % best_price)

            order = client.new_order(client_order_id, g_symbol, g_side, g_balance, best_price)
            if 'error' not in order:
                if order['status'] == 'filled':
                    print("Order filled", order)
                elif order['status'] == 'new' or order['status'] == 'partiallyFilled':
                    print("Waiting order...")

                TradeRecord.objects.create(clientOrderId=client_order_id, symbol=g_symbol, side=g_side,
                                           quantity=g_balance, price=best_price, now_status=order['status'])
            else:
                print(order['error'])

    else:
        if TradeRecord.objects.filter(now_status='new').exists():
            x = TradeRecord.objects.get(now_status='new')
            if x.wait_counter > 15 and x.side == 'buy':
                client.cancel_order(open_orders[0]["clientOrderId"])
                x.now_status = 'cancel'
            elif x.wait_counter > 45 and x.side == 'sell':
                client.cancel_order(open_orders[0]["clientOrderId"])
                x.now_status = 'cancel'
            else:
                x.wait_counter = x.wait_counter + 1
            x.save()
    return


def coin_home(request):
    my_profile = Profile.objects.get(user__username='guangyaw')
    session = requests.session()
    session.auth = (my_profile.api_key, my_profile.secret_no)
    b = session.get('https://api.hitbtc.com/api/2/trading/balance').json()
    mybalances = []
    for balances in b:
        if balances["available"] != '0':
            mybalances.append(balances)

    return render(request, "blogs/blog_home.html", {"balance": mybalances, "title": 'test balance'})


def auto_trade():
    print('auto_trade  .......')
    g_symbol = 'ETHBTC'

    my_profile = Profile.objects.get(user__username='guangyaw')
    client = Client("https://api.hitbtc.com", my_profile.api_key, my_profile.secret_no)
    eth_btc = client.get_symbol(g_symbol)
    orderbook = client.get_orderbook(g_symbol)
    # set
    order_avg = (float(orderbook['bid'][0]['price']) + float(orderbook['ask'][0]['price']))/2
    best_price = order_avg

    print('Current price: %s' % (best_price,))
    #
    best_counts = BestValues.objects.all().count()
    if best_counts < 10:
        #print(best_counts)
        BestValues.objects.create(symbol=g_symbol, best_price=str(best_price),
                                  best_bid=orderbook['bid'][0]['price'],
                                  best_ask=orderbook['ask'][0]['price'],
                                  timestamp=datetime.datetime.now())
    else:
        check_data = BestValues.objects.get(id=BestValues.objects.all()[0].id)
        if check_data.start_point == 99:
            check_data.start_point = 8  # next index
            check_data.save()
            tmp = BestValues.objects.get(id=BestValues.objects.all()[9].id)
        else:
            tmp = BestValues.objects.get(id=BestValues.objects.all()[check_data.start_point].id)

        tmp.symbol = g_symbol
        tmp.best_price = best_price
        tmp.best_bid = orderbook['bid'][0]['price']
        tmp.best_ask = orderbook['ask'][0]['price']
        tmp.timestamp = datetime.datetime.now()
        tmp.save()

        # define next index into BestValues.objects.all()[0]
        if check_data.start_point == 0:
            check_data.start_point = 9
        else:
            check_data.start_point = check_data.start_point - 1  # next index
        next_turn = BestValues.objects.get(id=BestValues.objects.all()[0].id)
        next_turn.start_point = check_data.start_point
        # print(next_turn.start_point)
        next_turn.save()

    # print('should into check_open_and_auto_trade ')
    check_open_and_auto_trade()


def auto_trade_start(request):
    if Schedule.objects.filter(name='send_auto_trade').exists():
        return HttpResponse('auto trade is exist')
    else:
        g_symbol = 'ETHBTC'

        my_profile = Profile.objects.get(user__username='guangyaw')
        client = Client("https://api.hitbtc.com", my_profile.api_key, my_profile.secret_no)
        eth_btc = client.get_symbol(g_symbol)
        # get trading balance
        eth_balance = 0.0
        btc_balance = 0.0
        balances = client.get_trading_balance()
        for balance in balances:
            if balance['currency'] == 'ETH':
                eth_balance = float(balance['available'])
            if balance['currency'] == 'BTC':
                btc_balance = float(balance['available'])

        orderbook = client.get_orderbook(g_symbol)
        order_avg = (Decimal(orderbook['bid'][0]['price']) + Decimal(orderbook['ask'][0]['price'])) / 2
        best_price = Decimal(order_avg)

        btc_balance_toETH = round(btc_balance / float(best_price), 4) - float(eth_btc['quantityIncrement'])
        print('Current BTC balance in ETH: %s ' % (btc_balance_toETH,))
        print('Current ETH balance: %s' % eth_balance)
        if btc_balance_toETH > eth_balance:
            base_amount = btc_balance_toETH
        else:
            base_amount = eth_balance
        print('PreOrder create')
        now_time = datetime.datetime.now()

        Schedule.objects.create(
            func='coins.views.auto_trade',
            name='send_auto_trade',
            repeats=-1,
            schedule_type=Schedule.MINUTES,
            # minutes=1,
            # next_run=next_turn
        )
        PreOrder.objects.create(symbol=g_symbol, base_amount=str(base_amount), status='running',
                                timestamp=now_time)

        return HttpResponse('auto trade start')


def auto_trade_stop(request):
    if Schedule.objects.filter(name='send_auto_trade').exists():
        Schedule.objects.get(name='send_auto_trade').delete()
        g_symbol = 'ETHBTC'

        my_profile = Profile.objects.get(user__username='guangyaw')
        client = Client("https://api.hitbtc.com", my_profile.api_key, my_profile.secret_no)
        eth_btc = client.get_symbol(g_symbol)
        # get trading balance
        eth_balance = 0.0
        btc_balance = 0.0
        balances = client.get_trading_balance()
        for balance in balances:
            if balance['currency'] == 'ETH':
                eth_balance = float(balance['available'])
            if balance['currency'] == 'BTC':
                btc_balance = float(balance['available'])

        orderbook = client.get_orderbook(g_symbol)
        order_avg = (Decimal(orderbook['bid'][0]['price']) + Decimal(orderbook['ask'][0]['price'])) / 2
        best_price = Decimal(order_avg)

        btc_balance_toETH = round(btc_balance / float(best_price), 4) - float(eth_btc['quantityIncrement'])
        print('Current BTC balance in ETH: %s ' % (btc_balance_toETH,))
        print('Current ETH balance: %s' % eth_balance)
        if btc_balance_toETH > eth_balance:
            end_amount = btc_balance_toETH
        else:
            end_amount = eth_balance
        print(end_amount)
        x = PreOrder.objects.get(status='running')
        x.status = 'stop'
        x.end_amount = str(end_amount)
        x.save()
        # cancel still open orders
        open_orders = client.get_open_order()
        if TradeRecord.objects.filter(now_status='new').exists():
            y = TradeRecord.objects.get(now_status='new')
            client.cancel_order(open_orders[0]["clientOrderId"])
            y.now_status = 'cancel'
            y.save()

    return HttpResponse('auto trade stop')


def ethbtc_sell(request):
    g_symbol = 'ETHBTC'

    my_profile = Profile.objects.get(user__username='guangyaw')
    client = Client("https://api.hitbtc.com", my_profile.api_key, my_profile.secret_no)
    eth_btc = client.get_symbol(g_symbol)

    # get eth trading balance
    eth_balance = 0.0
    balances = client.get_trading_balance()
    for balance in balances:
        if balance['currency'] == 'ETH':
            eth_balance = float(balance['available'])

    print('Current ETH balance: %s' % eth_balance)

    # sell eth at the best price
    if eth_balance >= float(eth_btc['quantityIncrement']):
        client_order_id = uuid.uuid4().hex
        orderbook = client.get_orderbook(g_symbol)
        # set price a little high
        #best_price = Decimal(orderbook['bid'][0]['price']) + Decimal(eth_btc['tickSize'])
        #best_price = Decimal(orderbook['ask'][0]['price']) - Decimal(eth_btc['tickSize'])
        order_avg = (Decimal(orderbook['bid'][0]['price']) + Decimal(orderbook['ask'][0]['price'])) / 2
        best_price = Decimal(order_avg)

        print("Selling at %s" % best_price)

        order = client.new_order(client_order_id, g_symbol, 'sell', eth_balance, best_price)
        if 'error' not in order:
            if order['status'] == 'filled':
                print("Order filled", order)
            elif order['status'] == 'new' or order['status'] == 'partiallyFilled':
                print("Waiting order...")
                for k in range(0, 3):
                    order = client.get_order(client_order_id, 20000)
                    print(order)

                    if 'error' in order or ('status' in order and order['status'] == 'filled'):
                        break

                # cancel order if it isn't filled
                # if 'status' in order and order['status'] != 'filled':
                #     cancel = client.cancel_order(client_order_id)
                #     print('Cancel order result', cancel)
        else:
            print(order['error'])

        return HttpResponse(order['status'])
    else:
        return HttpResponse('balance is not enough')


def ethbtc_buy(request):
    g_symbol = 'ETHBTC'

    my_profile = Profile.objects.get(user__username='guangyaw')
    client = Client("https://api.hitbtc.com", my_profile.api_key, my_profile.secret_no)
    eth_btc = client.get_symbol(g_symbol)

    # get btc trading balance
    eth_balance = 0.0
    balances = client.get_trading_balance()
    for balance in balances:
        if balance['currency'] == 'BTC':
            btc_balance = float(balance['available'])

    orderbook = client.get_orderbook(g_symbol)
    # set price a little high
    # best_price = Decimal(orderbook['ask'][0]['price']) - Decimal(eth_btc['tickSize'])
    # best_price = Decimal(orderbook['bid'][0]['price']) + Decimal(eth_btc['tickSize'])
    order_avg = (Decimal(orderbook['bid'][0]['price']) + Decimal(orderbook['ask'][0]['price'])) / 2
    best_price = Decimal(order_avg)

    btc_balance_toETH = round(btc_balance/float(best_price), 4) - float(eth_btc['quantityIncrement'])
    print('Current BTC balance: %s ,buy ETH: %s' % (btc_balance, btc_balance_toETH))

    # buy eth at the best price
    if btc_balance_toETH >= float(eth_btc['quantityIncrement']):
        client_order_id = uuid.uuid4().hex

        print(" at %s" % best_price)

        order = client.new_order(client_order_id, g_symbol, 'buy', btc_balance_toETH, best_price)
        if 'error' not in order:
            if order['status'] == 'filled':
                print("Order filled", order)
            elif order['status'] == 'new' or order['status'] == 'partiallyFilled':
                print("Waiting order...")
                for k in range(0, 3):
                    order = client.get_order(client_order_id, 20000)
                    print(order)

                    if 'error' in order or ('status' in order and order['status'] == 'filled'):
                        break
        else:
            print(order['error'])

        return HttpResponse('done')
    else:
        return HttpResponse('balance is not enough')

    return HttpResponse('price:'+str(best_price)+'amount:'+str(btc_balance_toETH))


def order_check(request):
    g_symbol = 'ETHBTC'

    my_profile = Profile.objects.get(user__username='guangyaw')
    client = Client("https://api.hitbtc.com", my_profile.api_key, my_profile.secret_no)
    eth_btc = client.get_symbol(g_symbol)

    orderbook = client.get_orderbook(g_symbol)
    # # set
    order_avg = (Decimal(orderbook['bid'][0]['price']) + Decimal(orderbook['ask'][0]['price'])) / 2
    best_price = Decimal(order_avg)

    print('Current price: %s' % (best_price,))
    #
    # best_counts = BestValues.objects.all().count()
    #
    # if best_counts < 10:
    #     print(type(orderbook["timestamp"]))
    #     #tmptime = datetime.strptime(orderbook['bid']["timestamp"].isoformat(), '%Y-%m-%d %H:%M:%S.%f')
    #     best_values = BestValues.objects.create(symbol=g_symbol, best_price=best_price,
    #                                                     best_bid=orderbook['bid'][0]['price'],
    #                                                     best_ask=orderbook['ask'][0]['price'],
    #                                                     timestamp=datetime.now())
    # else:
    #     check_data = BestValues.objects.get(id=BestValues.objects.all()[0].id)
    #     if check_data.start_point == 99:
    #         check_data.start_point = 8  # next index
    #         check_data.save()
    #         tmp = BestValues.objects.get(id=BestValues.objects.all()[9].id)
    #     else:
    #         tmp = BestValues.objects.get(id=BestValues.objects.all()[check_data.start_point].id)

        # tmp.symbol = g_symbol
        # tmp.best_price = best_price
        # tmp.best_bid = orderbook['bid'][0]['price']
        # tmp.best_ask = orderbook['ask'][0]['price']
        # tmp.timestamp = datetime.now()
        # tmp.save()

        # define next index into BestValues.objects.all()[0]
        # if check_data.start_point == 0:
        #     check_data.start_point = 9
        # else:
        #     check_data.start_point = check_data.start_point - 1  # next index
        # next_turn = BestValues.objects.get(id=BestValues.objects.all()[0].id)
        # next_turn.start_point = check_data.start_point
        # print(next_turn.start_point)
        # next_turn.save()
    best_values = BestValues.objects.all()

    data = {
        'title': g_symbol,
        'order': orderbook,
        'best_price': best_price,
        # 'best_bid': max_bid,
        # 'best_ask': min_ask,
        'best_values': best_values,
        'count': best_values[0].start_point,
    }
    return render(request, "coins/check_orders.html", data)

# offical sample code
# if __name__ == "__main__":
#     public_key = "ff20f250a7b3a414781d1abe11cd8cee"
#     secret = "fb453577d11294359058a9ae13c94713"
#
#     btc_address = "1ANJ18KJiL55adwzvNhRimnQcShR4iMvCe"
#
#     client = Client("https://api.hitbtc.com", public_key, secret)
#
#     eth_btc = client.get_symbol('ETHBTC')
#     address = client.get_address('ETH')     # get eth address for deposit
#
#     print('ETH deposit address: "%s"' % address)
#
#     # transfer all deposited eths from account to trading balance
#     balances = client.get_account_balance()
#     for balance in balances:
#         if balance['currency'] == 'ETH' and float(balance['available']) > float(eth_btc['quantityIncrement']):
#             client.transfer('ETH', balance['available'], True)
#             print('ETH Account balance: %s'% balance['available'])
#             time.sleep(1)   # wait till transfer completed
#
#     # get eth trading balance
#     eth_balance = 0.0
#     balances = client.get_trading_balance()
#     for balance in balances:
#         if balance['currency'] == 'ETH':
#             eth_balance = float(balance['available'])
#
#     print('Current ETH balance: %s' % eth_balance)
#
#     # sell eth at the best price
#     if eth_balance >= float(eth_btc['quantityIncrement']):
#         client_order_id = uuid.uuid4().hex
#         orderbook = client.get_orderbook('ETHBTC')
#         # set price a little high
#         best_price = Decimal(orderbook['bid'][0]['price']) + Decimal(eth_btc['tickSize'])
#
#         print("Selling at %s" % best_price)
#
#         order = client.new_order(client_order_id, 'ETHBTC', 'sell', eth_balance, best_price)
#         if 'error' not in order:
#             if order['status'] == 'filled':
#                 print("Order filled", order)
#             elif order['status'] == 'new' or order['status'] == 'partiallyFilled':
#                 print("Waiting order...")
#                 for k in range(0, 3):
#                     order = client.get_order(client_order_id, 20000)
#                     print(order)
#
#                     if 'error' in order or ('status' in order and order['status'] == 'filled'):
#                         break
#
#                 # cancel order if it isn't filled
#                 if 'status' in order and order['status'] != 'filled':
#                     cancel = client.cancel_order(client_order_id)
#                     print('Cancel order result', cancel)
#         else:
#             print(order['error'])
#
#     # transfer all available BTC after trading to account balance
#     balances = client.get_trading_balance()
#     for balance in balances:
#         if balance['currency'] == 'BTC':
#             transfer = client.transfer('BTC', balance['available'], False)
#             print('Transfer', transfer)
#             time.sleep(1)
#
#     # get account balance and withdraw BTC
#     balances = client.get_account_balance()
#     for balance in balances:
#         if balance['currency'] == 'BTC' and float(balance['available']) > 0.101:
#             payout = client.withdraw('BTC', '0.1', btc_address, '0.0005')
#
#             if 'error' not in payout:
#                 transaction_id = payout['id']
#                 print("Transaction ID: %s" % transaction_id)
#                 for k in range(0, 5):
#                     time.sleep(20)
#                     transaction = client.get_transaction(transaction_id)
#                     print("Payout info", transaction)
#             else:
#                 print(payout['error'])
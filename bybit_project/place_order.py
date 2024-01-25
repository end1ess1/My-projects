# def place_order(order_type):
#     if order_type == 'Buy':
#         order = session.place_order(
#             category='linear',
#             symbol=SYMBOL,
#             side=order_type,
#             orderType='Market',
#             qty=QNTY,
#             isLeverage=1
#         )
#         print(datetime.now(), 'Opened Long:', SYMBOL, QNTY, sep=' ')
#     if order_type == 'Sell':
#         order = session.place_order(
#             category='linear',
#             symbol=SYMBOL,
#             side=order_type,
#             orderType='Market',
#             qty=QNTY,
#             isLeverage=1
#         )
#         print(datetime.now(), 'Opened Short:', SYMBOL, QNTY, sep=' ')

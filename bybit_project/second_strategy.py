from datetime import datetime
import numpy as np
from vars import atr_klines_body, trend_flg, order_id_2, active_order_2, take_profit_2, sell_stop_2
from coin_info import SYMBOL
from klines_info_defs import load_to_txt
from time import sleep


def increased_volume_plus_trend(volume_condition, data):
    global order_id_2, active_order_2, take_profit_2, sell_stop_2

    data = list(map(float, data))

    if active_order_2 == 1:
        if data[2] >= take_profit_2:
            print('CLOSE SECOND STRATEGY')
            active_order_2 = 0
            load_to_txt('SECOND STRATEGY', order_id_2, SYMBOL, 'CLOSE', 'SELL', 'TAKE PROFIT', take_profit_2, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

        if data[3] <= sell_stop_2:
            print('CLOSE SECOND STRATEGY')
            active_order_2 = 0
            load_to_txt('SECOND STRATEGY', order_id_2, SYMBOL, 'CLOSE', 'SELL', 'STOP LOSS', sell_stop_2, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    elif active_order_2 == 2:
        if data[3] <= take_profit_2:
            print('CLOSE SECOND STRATEGY')
            active_order_2 = 0
            load_to_txt('SECOND STRATEGY', order_id_2, SYMBOL, 'CLOSE', 'BUY', 'TAKE PROFIT', take_profit_2, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

        if data[2] >= sell_stop_2:
            print('CLOSE SECOND STRATEGY')
            active_order_2 = 0
            load_to_txt('SECOND STRATEGY', order_id_2, SYMBOL, 'CLOSE', 'BUY', 'STOP LOSS', sell_stop_2, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    elif data[5] > volume_condition:
        if data[4] - data[1] > 0 and trend_flg == 1 and active_order_2 == 0:
            print('OPEN SECOND STRATEGY')
            order_id_2 += 1
            active_order_2 = 1
            take_profit_2 = np.round(data[4] + atr_klines_body, 3)
            sell_stop_2 = np.round(data[1] - atr_klines_body, 3)
            load_to_txt('SECOND STRATEGY', order_id_2, SYMBOL, 'OPEN', 'BUY', data[4], str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

            sleep(60)

        if data[4] - data[1] < 0 and trend_flg == -1 and active_order_2 == 0:
            print('OPEN SECOND STRATEGY')
            order_id_2 += 1
            active_order_2 = 2
            take_profit_2 = np.round(data[4] - atr_klines_body, 3)
            sell_stop_2 = np.round(data[1] + atr_klines_body, 3)
            load_to_txt('SECOND STRATEGY', order_id_2, SYMBOL, 'OPEN', 'SELL', data[4], str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

            sleep(60)

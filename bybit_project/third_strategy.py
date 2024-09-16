from datetime import datetime
from vars import atr_klines_body, order_id_3, take_profit_3, sell_stop_3, active_order_3, temporary_klines, trend_flg
from coin_info import SYMBOL
from klines_info_defs import load_to_txt


def absorption_of_prev_kline(data_klines):
    global order_id_3, take_profit_3, sell_stop_3, active_order_3, temporary_klines

    if (abs(float(data_klines[1][4]) - float(data_klines[1][1])) > abs(
            float(data_klines[2][2]) - float(data_klines[2][3])) * 1.25) and (
            float(data_klines[2][4]) - float(data_klines[2][1]) > 0 and float(data_klines[1][4]) - float(
        data_klines[1][1]) < 0) and (
            active_order_3 == 0) and (data_klines[1] != temporary_klines):
        print('OPEN THIRD STRATEGY')
        temporary_klines = data_klines[1]
        order_id_3 += 1
        active_order_3 = 1
        take_profit_3 = float(data_klines[1][4]) - atr_klines_body
        sell_stop_3 = float(
            data_klines[1][4]) + abs(float(data_klines[1][4]) - float(data_klines[1][1])) * 0.7
        load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'OPEN', 'SELL', data_klines[1][4], str(
            datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if (abs(float(data_klines[1][4]) - float(data_klines[1][1])) > abs(
            float(data_klines[2][4]) - float(data_klines[2][1])) * 1.5) and (
            float(data_klines[2][4]) - float(data_klines[2][1]) < 0 and float(data_klines[1][4]) - float(
        data_klines[1][1]) > 0) and (
            active_order_3 == 0) and (data_klines[1] != temporary_klines):
        temporary_klines = data_klines[1]
        print('OPEN THIRD STRATEGY')
        order_id_3 += 1
        active_order_3 = 2
        take_profit_3 = float(data_klines[1][4]) + atr_klines_body
        sell_stop_3 = float(
            data_klines[1][4]) - abs(float(data_klines[1][4]) - float(data_klines[1][1])) * 0.7
        load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'OPEN', 'BUY', data_klines[1][4], str(
            datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if active_order_3 == 1:
        if float(data_klines[0][4]) <= take_profit_3:
            print('CLOSE THIRD STRATEGY')
            active_order_3 = 0
            load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'CLOSE', 'BUY', 'TAKE PROFIT', take_profit_3, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

        elif float(data_klines[0][4]) >= sell_stop_3:
            print('CLOSE THIRD STRATEGY')
            active_order_3 = 0
            load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'CLOSE', 'BUY', 'STOP LOSS', sell_stop_3, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if active_order_3 == 2:
        if float(data_klines[0][4]) >= take_profit_3:
            print('CLOSE THIRD STRATEGY')
            active_order_3 = 0
            load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'CLOSE', 'SELL', 'TAKE PROFIT', take_profit_3, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

        elif float(data_klines[0][4]) <= sell_stop_3:
            print('CLOSE THIRD STRATEGY')
            active_order_3 = 0
            load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'CLOSE', 'SELL', 'STOP LOSS', sell_stop_3, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])


def new_absorption_of_prev_kline(data_klines):
    global order_id_3, take_profit_3, sell_stop_3, active_order_3, temporary_klines, trend_flg

    if (abs(float(data_klines[1][4]) - float(data_klines[1][1])) > abs(
            float(data_klines[2][2]) - float(data_klines[2][3])) * 1.5) and (
            float(data_klines[2][4]) - float(data_klines[2][1]) > 0 and float(data_klines[1][4]) - float(
        data_klines[1][1]) < 0) and (
            active_order_3 == 0) and (data_klines[1] != temporary_klines) and (trend_flg == -1):
        print('OPEN THIRD STRATEGY')
        temporary_klines = data_klines[1]
        order_id_3 += 1
        active_order_3 = 1
        take_profit_3 = float(data_klines[1][4]) - atr_klines_body
        sell_stop_3 = float(
            data_klines[1][4]) + abs(float(data_klines[1][4]) - float(data_klines[1][1])) * 0.7
        load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'OPEN', 'SELL', data_klines[1][4], str(
            datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if (abs(float(data_klines[1][4]) - float(data_klines[1][1])) > abs(
            float(data_klines[2][4]) - float(data_klines[2][1])) * 1.5) and (
            float(data_klines[2][4]) - float(data_klines[2][1]) < 0 and float(data_klines[1][4]) - float(
        data_klines[1][1]) > 0) and (
            active_order_3 == 0) and (data_klines[1] != temporary_klines) and (trend_flg == 1):
        print('OPEN THIRD STRATEGY')
        temporary_klines = data_klines[1]
        order_id_3 += 1
        active_order_3 = 2
        take_profit_3 = float(data_klines[1][4]) + atr_klines_body
        sell_stop_3 = float(
            data_klines[1][4]) - abs(float(data_klines[1][4]) - float(data_klines[1][1])) * 0.7
        load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'OPEN', 'BUY', data_klines[1][4], str(
            datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if active_order_3 == 1:

        if float(data_klines[0][4]) <= take_profit_3:
            print('CLOSE THIRD STRATEGY')
            active_order_3 = 0
            load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'CLOSE', 'BUY', 'TAKE PROFIT', take_profit_3, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

        elif float(data_klines[0][4]) >= sell_stop_3:
            print('CLOSE THIRD STRATEGY')
            active_order_3 = 0
            load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'CLOSE', 'BUY', 'STOP LOSS', sell_stop_3, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if active_order_3 == 2:

        if float(data_klines[0][4]) >= take_profit_3:
            print('CLOSE THIRD STRATEGY')
            active_order_3 = 0
            load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'CLOSE', 'SELL', 'TAKE PROFIT', take_profit_3, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

        elif float(data_klines[0][4]) <= sell_stop_3:
            print('CLOSE THIRD STRATEGY')
            active_order_3 = 0
            load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'CLOSE', 'SELL', 'STOP LOSS', sell_stop_3, str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

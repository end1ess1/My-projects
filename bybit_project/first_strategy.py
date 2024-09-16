from datetime import datetime
import numpy as np
from coin_info import SYMBOL
from klines_info_defs import load_to_txt
from vars import active_sell_order_1, order_id_1, temporary_sell_order_id_1, sell_stop_loss_1, sell_take_profit_1, \
    sell_temporary_data_1, trend_flg
from vars import atr_klines_body, active_buy_order_1, order_id_1, temporary_buy_order_id_1, buy_stop_loss_1, \
    buy_take_profit_1, buy_temporary_data_1
from coin_info import step


def several_same_high_prices(klines_data):
    # klines_data[*][1] -> Open Price         ||         klines_data[0][*] -> first(right now) kline
    # klines_data[*][2] -> Highest Price      ||         klines_data[1][*] -> second kline
    # klines_data[*][3] -> Lowest Price       ||         klines_data[2][*] -> third kline
    # klines_data[*][4] -> Close Price        ||         klines_data[3][*] -> fourth kline

    global active_sell_order_1, order_id_1, temporary_sell_order_id_1, sell_stop_loss_1, sell_take_profit_1, sell_temporary_data_1, step

    if (klines_data[1][2] == klines_data[2][2]) and (active_sell_order_1 == False) and (
    klines_data[1][2], klines_data[2][2]) not in sell_temporary_data_1:
        sell_temporary_data_1.append((klines_data[1][2], klines_data[2][2]))
        order_id_1 += 1
        temporary_sell_order_id_1 = order_id_1
        active_sell_order_1 = True
        sell_stop_loss_1 = np.round(float(klines_data[1][2]) + step, 3)
        print('OPEN FIRST STRATEGY')
        sell_take_profit_1 = np.round(
            float(klines_data[1][4]) - atr_klines_body * 2, 3)
        load_to_txt('FIRST STRATEGY', temporary_sell_order_id_1, SYMBOL, 'OPEN', 'SELL', klines_data[1][4], str(
            datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if (float(klines_data[0][2]) >= sell_stop_loss_1) and (active_sell_order_1 == True):
        print('CLOSE FIRST STRATEGY')
        active_sell_order_1 = False
        load_to_txt('FIRST STRATEGY', temporary_sell_order_id_1, SYMBOL, 'CLOSE', 'BUY', 'STOP LOSS',
                    sell_stop_loss_1, str(datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if (float(klines_data[0][3]) <= sell_take_profit_1) and (active_sell_order_1 == True):
        print('CLOSE FIRST STRATEGY')
        active_sell_order_1 = False
        load_to_txt('FIRST STRATEGY', temporary_sell_order_id_1, SYMBOL, 'CLOSE', 'BUY', 'TAKE PROFIT',
                    sell_take_profit_1, str(datetime.now())[:10], str(datetime.time(datetime.now()))[:9])


def several_same_low_prices(klines_data):
    # klines_data[*][1] -> Open Price         ||         klines_data[0][*] -> first(right now) kline
    # klines_data[*][2] -> Highest Price      ||         klines_data[1][*] -> second kline
    # klines_data[*][3] -> Lowest Price       ||         klines_data[2][*] -> third kline
    # klines_data[*][4] -> Close Price        ||         klines_data[3][*] -> fourth kline

    global active_buy_order_1, order_id_1, temporary_buy_order_id_1, buy_stop_loss_1, buy_take_profit_1, buy_temporary_data_1, step

    if (klines_data[1][3] == klines_data[2][3]) and (active_buy_order_1 == False) and (
    klines_data[1][3], klines_data[2][3]) not in buy_temporary_data_1:
        buy_temporary_data_1.append((klines_data[1][3], klines_data[2][3]))
        order_id_1 += 1
        active_buy_order_1 = True
        temporary_buy_order_id_1 = order_id_1
        buy_stop_loss_1 = np.round(float(klines_data[1][3]) - step, 3)
        buy_take_profit_1 = np.round(
            float(klines_data[1][4]) + atr_klines_body * 2, 3)
        print('OPEN FIRST STRATEGY')
        load_to_txt('FIRST STRATEGY', temporary_buy_order_id_1, SYMBOL, 'OPEN', 'BUY', klines_data[1][4], str(
            datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if (float(klines_data[0][3]) <= buy_stop_loss_1) and (active_buy_order_1 == True):
        print('CLOSE FIRST STRATEGY')
        active_buy_order_1 = False
        load_to_txt('FIRST STRATEGY', temporary_buy_order_id_1, SYMBOL, 'CLOSE', 'SELL', 'STOP LOSS',
                    buy_stop_loss_1, str(datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if (float(klines_data[0][2]) >= buy_take_profit_1) and (active_buy_order_1 == True):
        print('CLOSE FIRST STRATEGY')
        active_buy_order_1 = False
        load_to_txt('FIRST STRATEGY', temporary_buy_order_id_1, SYMBOL, 'CLOSE', 'SELL', 'TAKE PROFIT',
                    buy_take_profit_1, str(datetime.now())[:10], str(datetime.time(datetime.now()))[:9])


def new_several_same_high_prices(klines_data):
    # klines_data[*][1] -> Open Price         ||         klines_data[0][*] -> first(right now) kline
    # klines_data[*][2] -> Highest Price      ||         klines_data[1][*] -> second kline
    # klines_data[*][3] -> Lowest Price       ||         klines_data[2][*] -> third kline
    # klines_data[*][4] -> Close Price        ||         klines_data[3][*] -> fourth kline

    global active_sell_order_1, order_id_1, temporary_sell_order_id_1, sell_stop_loss_1, sell_take_profit_1, sell_temporary_data_1, step, trend_flg

    if (klines_data[1][2] == klines_data[2][2]) and (klines_data[2][2] == klines_data[3][2]) and (
            active_sell_order_1 == False) and (
            (klines_data[1][2], klines_data[2][2]) not in sell_temporary_data_1) and (trend_flg == -1):
        sell_temporary_data_1.append((klines_data[1][2], klines_data[2][2]))
        order_id_1 += 1
        temporary_sell_order_id_1 = order_id_1
        active_sell_order_1 = True
        sell_stop_loss_1 = np.round(float(klines_data[1][2]) + step, 3)
        print('OPEN FIRST STRATEGY')
        sell_take_profit_1 = np.round(
            float(klines_data[1][4]) - atr_klines_body * 2, 3)
        load_to_txt('FIRST STRATEGY', temporary_sell_order_id_1, SYMBOL, 'OPEN', 'SELL', klines_data[1][4], str(
            datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if (float(klines_data[0][2]) >= sell_stop_loss_1) and (active_sell_order_1 == True):
        print('CLOSE FIRST STRATEGY')
        active_sell_order_1 = False
        load_to_txt('FIRST STRATEGY', temporary_sell_order_id_1, SYMBOL, 'CLOSE', 'BUY', 'STOP LOSS',
                    sell_stop_loss_1, str(datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if (float(klines_data[0][3]) <= sell_take_profit_1) and (active_sell_order_1 == True):
        print('CLOSE FIRST STRATEGY')
        active_sell_order_1 = False
        load_to_txt('FIRST STRATEGY', temporary_sell_order_id_1, SYMBOL, 'CLOSE', 'BUY', 'TAKE PROFIT',
                    sell_take_profit_1, str(datetime.now())[:10], str(datetime.time(datetime.now()))[:9])


def new_several_same_low_prices(klines_data):
    # klines_data[*][1] -> Open Price         ||         klines_data[0][*] -> first(right now) kline
    # klines_data[*][2] -> Highest Price      ||         klines_data[1][*] -> second kline
    # klines_data[*][3] -> Lowest Price       ||         klines_data[2][*] -> third kline
    # klines_data[*][4] -> Close Price        ||         klines_data[3][*] -> fourth kline

    global active_buy_order_1, order_id_1, temporary_buy_order_id_1, buy_stop_loss_1, buy_take_profit_1, buy_temporary_data_1, step, trend_flg

    if (klines_data[1][3] == klines_data[2][3]) and (klines_data[2][3] == klines_data[3][3]) and (
            active_buy_order_1 == False) and ((klines_data[1][3], klines_data[2][3]) not in buy_temporary_data_1) and (
            trend_flg == 1):
        buy_temporary_data_1.append((klines_data[1][3], klines_data[2][3]))
        order_id_1 += 1
        active_buy_order_1 = True
        temporary_buy_order_id_1 = order_id_1
        buy_stop_loss_1 = np.round(float(klines_data[1][3]) - step, 3)
        buy_take_profit_1 = np.round(
            float(klines_data[1][4]) + atr_klines_body * 2, 3)
        print('OPEN FIRST STRATEGY')
        load_to_txt('FIRST STRATEGY', temporary_buy_order_id_1, SYMBOL, 'OPEN', 'BUY', klines_data[1][4], str(
            datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if (float(klines_data[0][3]) <= buy_stop_loss_1) and (active_buy_order_1 == True):
        print('CLOSE FIRST STRATEGY')
        active_buy_order_1 = False
        load_to_txt('FIRST STRATEGY', temporary_buy_order_id_1, SYMBOL, 'CLOSE', 'SELL', 'STOP LOSS',
                    buy_stop_loss_1, str(datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if (float(klines_data[0][2]) >= buy_take_profit_1) and (active_buy_order_1 == True):
        print('CLOSE FIRST STRATEGY')
        active_buy_order_1 = False
        load_to_txt('FIRST STRATEGY', temporary_buy_order_id_1, SYMBOL, 'CLOSE', 'SELL', 'TAKE PROFIT',
                    buy_take_profit_1, str(datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

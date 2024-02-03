from pybit.unified_trading import HTTP
import numpy as np
from time import sleep
from datetime import datetime
from file import key, secret

# CONNECTION
session = HTTP(
    testnet = False,
    api_key = key,
    api_secret = secret
)

# COIN
SYMBOL = 'ARBUSDT'
INTERVAL = 1
INTERVAL_NAME = 'min'
step = 0.0001
time = '18:00:00'


# GET INFO ABOUT KLINES
def get_data(LIMIT):
    kline = session.get_kline(
        symbol=SYMBOL, interval=INTERVAL, limit=LIMIT)
    kline = kline['result']['list']
    return kline


def test_data(LIMIT):
    return [['1705773180000', '4.200', '4.396', '4.265', '4.276', '200171.5', '168040.1963'], ['1705773120000', '4.276', '4.285', '4.273', '4.200', '39583.4', '169420.5631'], ['1705773060000', '4.246', '4.284', '4.273', '4.276', '38160.4', '162870.2727'], ['1705773000000', '4.262', '4.263', '4.241', '4.246', '34169.6', '145193.9812'], ['1705772940000', '4.236', '4.268', '4.224', '4.262', '43849', '185968.8818'], ['1705772880000', '4.26', '4.286', '4.23', '4.236', '108976.5', '464323.2484'], ['1705772820000', '4.242', '4.265', '4.232', '4.26', '55434.3', '235477.3224'], ['1705772760000', '4.27', '4.273', '4.221', '4.242', '102886.3', '436922.3427'],
            ['1705772700000', '4.226', '4.316', '4.226', '4.27', '182327.7', '779776.1348'], ['1705772640000', '4.235', '4.246', '4.211', '4.226', '36840.8', '155680.2943'], ['1705772580000', '4.228', '4.248', '4.22', '4.235', '37305', '157962.8215'], ['1705772520000',
                                                                                                                                                                                                                                                             '4.194', '4.233', '4.171', '4.228', '115943.4', '487294.5912'], ['1705772460000', '4.246', '4.273', '4.189', '4.194', '131391.5', '555755.5167'], ['1705772400000', '4.219', '4.261', '4.219', '4.246', '88086.6', '373860.4757'], ['1705772340000', '4.273', '4.273', '4.203', '4.219', '236125', '1000713.4134'], ['1705772280000', '4.283', '4.301', '4.253', '4.273', '161129.2', '689003.2002'], ['1705772220000', '4.296', '4.323', '4.267', '4.283', '121943.3', '523811.6675'], ['1705772160000', '4.331', '4.349', '4.275', '4.296', '143310.8', '616126.1495'], ['1705772100000', '4.362', '4.369', '4.322', '4.331', '97304.9', '422574.5353'], ['1705772040000', '4.361', '4.364', '4.334', '4.362', '60048.7', '261280.0273'], ['1705771980000', '4.339', '4.369', '4.332', '4.361', '65885.3', '286958.4489'], ['1705771920000', '4.339', '4.349', '4.294', '4.339', '167057.9', '722210.4634'], ['1705771860000', '4.38', '4.397', '4.338', '4.339', '67097.3', '293324.5792'], ['1705771800000', '4.369', '4.389', '4.344', '4.38', '84927.2', '371286.5542'], ['1705771740000', '4.351', '4.369', '4.333', '4.369', '87685.7', '381900.9773'], ['1705771680000', '4.385', '4.369', '4.325', '4.351', '162639.4', '708234.7452'], ['1705771620000', '4.361', '4.405', '4.361', '4.385', '118105.5', '517698.3063'], ['1705771560000', '4.502', '4.503', '4.349', '4.361', '600293.5', '2643803.2165'], ['1705771500000', '4.524', '4.524', '4.5', '4.502',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     '38334.7', '173064.4631'], ['1705771440000', '4.525', '4.528', '4.517', '4.524', '12798.5', '57895.2392'], ['1705771380000', '4.519', '4.535', '4.505', '4.525', '39818.9', '179862.6952'], ['1705771320000', '4.548', '4.548', '4.51', '4.519', '39891.3', '180252.1987'], ['1705771260000', '4.533', '4.564', '4.532', '4.548', '50868.7', '231443.3271'], ['1705771200000', '4.521', '4.533', '4.514', '4.533', '43053.3', '194850.8699'], ['1705771140000', '4.533', '4.539', '4.513', '4.521', '21869.4', '98979.083'], ['1705771080000', '4.534', '4.542', '4.515', '4.533', '22643.6', '102512.901'], ['1705771020000', '4.551', '4.552', '4.525', '4.534', '21015.9', '95250.512'], ['1705770960000', '4.548', '4.567', '4.543', '4.551', '31960.3', '145663.2572'], ['1705770900000', '4.532', '4.549', '4.515', '4.548', '32107.9', '145482.9222'], ['1705770840000', '4.536', '4.55', '4.525', '4.532', '24855.6', '112797.9526'], ['1705770780000', '4.544', '4.544', '4.529', '4.536', '16245.9', '73671.264'], ['1705770720000', '4.558', '4.573', '4.53', '4.544', '31559.5', '143621.4751'], ['1705770660000', '4.561', '4.576', '4.554', '4.558', '29818.8', '136243.6469'], ['1705770600000', '4.534', '4.563', '4.531', '4.561', '34571.9', '157282.5012'], ['1705770540000', '4.543', '4.55', '4.532', '4.534', '35659.9', '161929.7069'], ['1705770480000', '4.534', '4.552', '4.524', '4.543', '38663.9', '175305.6982'], ['1705770420000', '4.571',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      '4.576', '4.532', '4.534', '78656.9', '357923.0105'], ['1705770360000', '4.576', '4.577', '4.56', '4.571', '57288.2', '261735.4081'], ['1705770300000', '4.581', '4.591', '4.571', '4.576', '39109.9', '179110.8192'], ['1705770240000', '4.601', '4.628', '4.58', '4.581', '75081.2', '345852.4222'], ['1705770180000', '4.596', '4.619', '4.58', '4.601', '47150.7', '217134.5259'], ['1705770120000', '4.61', '4.638', '4.593', '4.596', '111304', '514080.9538'], ['1705770060000', '4.576', '4.63', '4.554', '4.61', '120164.6', '552678.3531'], ['1705770000000', '4.539', '4.619', '4.52', '4.576', '174323.6', '797787.1366'], ['1705769940000', '4.524', '4.55', '4.518', '4.539', '67107.4', '304366.2129'], ['1705769880000', '4.517', '4.532', '4.517', '4.524', '39651.7', '179347.2453'], ['1705769820000', '4.523', '4.526', '4.51', '4.517', '26209.4', '118405.834'], ['1705769760000', '4.511', '4.541', '4.506', '4.523', '79842.7', '361472.794'], ['1705769700000', '4.486', '4.525', '4.48', '4.511', '38642.7', '174255.8307'], ['1705769640000', '4.458', '4.505', '4.452', '4.486', '70558.3', '316873.4582']]


def load_to_txt(*args):
    args = ' | '.join(list(map(str, args)))
    with open('bybit_data_b_test.txt', mode='a') as file:
        file.write(args+'\n')


# TREND


def trend(data):
    all_highest_prices = []
    all_lowest_prices = []
    for each in data[::-1]:
        all_highest_prices.append(each[2])
        all_lowest_prices.append(each[3])
    ma = max(all_highest_prices)
    mi = min(all_lowest_prices)
    print('HIGHEST: ', ma, 'LOWEST: ', mi)
    print('INDEX HIGHEST: ', all_highest_prices.index(ma),
          'INDEX LOWEST: ', all_lowest_prices.index(mi))
    if all_highest_prices.index(ma) < all_lowest_prices.index(mi):
        return -1
    else:
        return 1

# AVG VOLUME


def avg_volume(data):

    # klines_data[*][5] -> Kline volume         ||         klines_data[0][*] -> first(right now) kline
    all_volume = []
    for each in data:
        all_volume.append(float(each[5]))
    return np.mean(all_volume)

# VOLUME + TREND


def increased_volume_plus_trend(data):

    global order_id_2, active_order_2, take_profit_2, sell_stop_2, common_trend

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

    elif data[5] > avg_volume_last_hour*2:

        if data[4]-data[1] > 0 and common_trend == 1 and active_order_2 == 0:
            print('OPEN SECOND STRATEGY')
            order_id_2 += 1
            active_order_2 = 1
            take_profit_2 = np.round(data[4]+atr_klines_body, 3)
            sell_stop_2 = np.round(data[1]-atr_klines_body, 3)
            load_to_txt('SECOND STRATEGY', order_id_2, SYMBOL, 'OPEN', 'BUY', data[4], str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

            sleep(60)

        if data[4]-data[1] < 0 and common_trend == -1 and active_order_2 == 0:
            print('OPEN SECOND STRATEGY')
            order_id_2 += 1
            active_order_2 = 2
            take_profit_2 = np.round(data[4]-atr_klines_body, 3)
            sell_stop_2 = np.round(data[1]+atr_klines_body, 3)
            load_to_txt('SECOND STRATEGY', order_id_2, SYMBOL, 'OPEN', 'SELL', data[4], str(
                datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

            sleep(60)


# AVERAGE TRUE RANGE


def average_true_range(klines_data):
    klines_body = []
    klines_shadow = []
    for each in klines_data:
        klines_body.append(abs(float(each[1])-float(each[4])))
        klines_shadow.append(abs(float(each[2])-float(each[3])))
    return np.round(np.mean(np.array(klines_body)), 3), np.round(np.mean(np.array(klines_shadow)), 3)

# SEVERAL SAME HIGH PRICES


def several_same_high_prices(klines_data):

    # klines_data[*][1] -> Open Price         ||         klines_data[0][*] -> first(right now) kline
    # klines_data[*][2] -> Highest Price      ||         klines_data[1][*] -> second kline
    # klines_data[*][3] -> Lowest Price       ||         klines_data[2][*] -> third kline
    # klines_data[*][4] -> Close Price        ||         klines_data[3][*] -> fourth kline

    global active_sell_order_1, order_id_1, temporary_sell_order_id_1, sell_stop_loss_1, sell_take_profit_1, sell_temporary_data_1, step, common_trend

    if (klines_data[1][2] == klines_data[2][2]) and (klines_data[2][2] == klines_data[3][2]) and (active_sell_order_1 == False) and ((klines_data[1][2], klines_data[2][2]) not in sell_temporary_data_1) and (common_trend == -1):
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

    global active_buy_order_1, order_id_1, temporary_buy_order_id_1, buy_stop_loss_1, buy_take_profit_1, buy_temporary_data_1, step, common_trend

    if (klines_data[1][3] == klines_data[2][3]) and (klines_data[2][3] == klines_data[3][3]) and (active_buy_order_1 == False) and ((klines_data[1][3], klines_data[2][3]) not in buy_temporary_data_1) and (common_trend == 1):
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


def absorption_of_prev_kline(data_klines):

    global order_id_3, take_profit_3, sell_stop_3, active_order_3, temporary_klines, common_trend

    if (abs(float(data_klines[1][4])-float(data_klines[1][1])) > abs(float(data_klines[2][2])-float(data_klines[2][3]))*1.5) and (
            float(data_klines[2][4])-float(data_klines[2][1]) > 0 and float(data_klines[1][4])-float(data_klines[1][1]) < 0) and (
            active_order_3 == 0) and (data_klines[1] != temporary_klines) and (common_trend == -1):
        print('OPEN THIRD STRATEGY')
        temporary_klines = data_klines[1]
        order_id_3 += 1
        active_order_3 = 1
        take_profit_3 = float(data_klines[1][4]) - atr_klines_body
        sell_stop_3 = float(
            data_klines[1][4]) + abs(float(data_klines[1][4])-float(data_klines[1][1]))*0.7
        load_to_txt('THIRD STRATEGY', order_id_3, SYMBOL, 'OPEN', 'SELL', data_klines[1][4], str(
            datetime.now())[:10], str(datetime.time(datetime.now()))[:9])

    if (abs(float(data_klines[1][4])-float(data_klines[1][1])) > abs(float(data_klines[2][4])-float(data_klines[2][1]))*1.5) and (
            float(data_klines[2][4])-float(data_klines[2][1]) < 0 and float(data_klines[1][4])-float(data_klines[1][1]) > 0) and (
            active_order_3 == 0) and (data_klines[1] != temporary_klines) and (common_trend == 1):
        print('OPEN THIRD STRATEGY')
        temporary_klines = data_klines[1]
        order_id_3 += 1
        active_order_3 = 2
        take_profit_3 = float(data_klines[1][4]) + atr_klines_body
        sell_stop_3 = float(
            data_klines[1][4]) - abs(float(data_klines[1][4])-float(data_klines[1][1]))*0.7
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


# GENERAL VARS
global_data = get_data(1440)
atr_klines_body, atr_klines_shadow = average_true_range(global_data)
order_id_1 = 0


# VARS OF STRATEGY - SEVERAL SAME HIGH PRICES
active_sell_order_1 = False
temporary_sell_order_id_1 = 0
sell_stop_loss_1 = 999999
sell_take_profit_1 = 0
sell_temporary_data_1 = []

# VARS OF STRATEGY - SEVERAL SAME HIGH PRICES
active_buy_order_1 = False
temporary_buy_order_id_1 = 0
buy_stop_loss_1 = 0
buy_take_profit_1 = 999999
buy_temporary_data_1 = []

# VARS OF STRATEGY - VOLUME + TREND
order_id_2 = 0
active_order_2 = 0
common_trend = trend(global_data)
avg_volume_last_hour = avg_volume(get_data(60))
take_profit_2 = 0
sell_stop_2 = 0

# VARS OF STRATEGY - ABSORPTION PREV KLINE
order_id_3 = 0
sell_stop_3 = 0
take_profit_3 = 0
active_order_3 = 0
temporary_klines = ['1705772700000', '4.226', '4.316',
                    '4.226', '4.27', '182327.7', '779776.1348']

# MAIN PROGRAM


def main():

    print('\nBot started. Please Wait...')
    print('\nCOIN: ', SYMBOL, '\n')
    print('\nTIME FRAME: ', INTERVAL, INTERVAL_NAME, sep=' ')
    if common_trend == 1:
        print('\n↑↑↑ TREND UP ↑↑↑')
    else:
        print('\n↓↓↓ TREND DOWN ↓↓↓')
    print()
    print('AVG VOLUME LAST HOUR: ', avg_volume_last_hour)

    while True:
        # GET INFO ABOUT KLINES
        klines_data = get_data(60)

        print(str(datetime.time(datetime.now()))[:8], SYMBOL,
              'Looking for...', sep=' | ')

        # FIRST STRATEGY. SEVERAL SAME HIGH PRICES AND SEVERAL SAME LOW PRICES
        several_same_high_prices(klines_data[:4])
        several_same_low_prices(klines_data[:4])

        # SECOND STRATEGY. INCREASED VOLUME + TREND
        increased_volume_plus_trend(klines_data[0])

        # THIRD STRATEGY. ABSORPTION OF SEVERAL KLINES
        absorption_of_prev_kline(klines_data[:3])
        sleep(10)

    # with open('test_data.txt', mode='a') as a:
    #     for i in range(1, 13):
    #         for each_trade in diary[str(i)]:
    #             for each_parameter in each_trade:
    #                 a.write(str(each_parameter)+' ')
    #             a.write('\n')


if __name__ == '__main__':
    main()

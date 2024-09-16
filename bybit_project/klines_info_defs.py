import numpy as np
from private_file import session
from coin_info import SYMBOL, INTERVAL

def get_data(LIMIT):
    global session, SYMBOL, INTERVAL
    kline = session.get_kline(
        symbol=SYMBOL, interval=INTERVAL, limit=LIMIT)
    kline = kline['result']['list']
    return kline

def load_to_txt(*args):
    args = ' | '.join(list(map(str, args)))
    with open('bybit_data_a_test.txt', mode='a') as file:
        file.write(args + '\n')

def trend(data):
    all_highest_prices = []
    all_lowest_prices = []
    for each in data[::-1]:
        all_highest_prices.append(each[2])
        all_lowest_prices.append(each[3])
    ma = max(all_highest_prices)
    mi = min(all_lowest_prices)
    if all_highest_prices.index(ma) < all_lowest_prices.index(mi):
        return -1
    else:
        return 1

def avg_volume(data):
    # klines_data[*][5] -> Kline volume         ||         klines_data[0][*] -> first(right now) kline
    all_volume = []
    for each in data:
        all_volume.append(float(each[5]))
    return np.mean(all_volume)

def average_true_range(klines_data):
    klines_body = []
    klines_shadow = []
    for each in klines_data:
        klines_body.append(abs(float(each[1]) - float(each[4])))
        klines_shadow.append(abs(float(each[2]) - float(each[3])))
    return np.round(np.mean(np.array(klines_body)), 3), np.round(np.mean(np.array(klines_shadow)), 3)

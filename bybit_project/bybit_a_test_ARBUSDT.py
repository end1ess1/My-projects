from time import sleep
from datetime import datetime
from coin_info import SYMBOL, INTERVAL, INTERVAL_NAME
from first_strategy import several_same_high_prices, several_same_low_prices
from second_strategy import increased_volume_plus_trend
from third_strategy import absorption_of_prev_kline
from vars import trend_flg, avg_volume_last_hour, volume_condition_1
from klines_info_defs import get_data


# MAIN SCRIPT
def main():
    print(
        f'\nBot started. Please Wait...\nCOIN: {SYMBOL} \nTIME FRAME: {INTERVAL} {INTERVAL_NAME} \nAVG VOLUME LAST HOUR: {avg_volume_last_hour}')
    print('\n↑↑↑ TREND UP ↑↑↑') if trend_flg == 1 else print('\n↓↓↓ TREND DOWN ↓↓↓')

    while True:
        # GET INFO ABOUT KLINES
        klines_data = get_data(60)

        print(str(datetime.time(datetime.now()))[:8], SYMBOL,
              'Looking for...', sep=' | ')

        # FIRST STRATEGY. SEVERAL SAME HIGH PRICES AND SEVERAL SAME LOW PRICES
        several_same_high_prices(klines_data[:3])
        several_same_low_prices(klines_data[:3])

        # SECOND STRATEGY. INCREASED VOLUME + TREND
        increased_volume_plus_trend(volume_condition_1, klines_data[0])

        # THIRD STRATEGY. ABSORPTION OF SEVERAL KLINES
        absorption_of_prev_kline(klines_data[:3])

        # PARSING KLINE DATA EVERY 10 SEC
        sleep(10)


if __name__ == '__main__':
    main()

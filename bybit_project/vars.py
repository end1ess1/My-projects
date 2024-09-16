from klines_info_defs import get_data, average_true_range, trend, avg_volume

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
trend_flg = trend(global_data)
avg_volume_last_hour = avg_volume(get_data(60))
take_profit_2 = 0
sell_stop_2 = 0
volume_condition_1 = avg_volume_last_hour * 1.5
volume_condition_2 = avg_volume_last_hour * 2

# VARS OF STRATEGY - ABSORPTION PREV KLINE
order_id_3 = 0
sell_stop_3 = 0
take_profit_3 = 0
active_order_3 = 0
temporary_klines = ['1705772700000', '4.226', '4.316',
                    '4.226', '4.27', '182327.7', '779776.1348']

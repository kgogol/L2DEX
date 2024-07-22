import numpy as np

def calculate_metrics(merged_df):
    def calculateV_MAX(reserves_y, price_AMM, price_CEX):
        return abs((reserves_y * (price_AMM - price_CEX) / (2 * price_AMM)))

    def calculateMAV(reserves_y, price_AMM, price_CEX):
        return (reserves_y * (price_AMM - price_CEX) ** 2 / (4 * price_AMM))

    merged_df['MAV_0'] = calculateMAV(merged_df['reserve_1'], merged_df['spot_price'], merged_df['CEX_price'])

    merged_df['V_max_1'] = calculateV_MAX(merged_df['reserve_1'], merged_df['spot_price'], merged_df['CEX_price'])
    merged_df['V_max_0'] = merged_df['V_max_1'] * merged_df['spot_price']

    merged_df['reserve_total_0'] = 2 * merged_df['reserve_0']  # that works only for Uniswap v2 (and its forks)
    #merged_df['price_diff'] = merged_df['spot_price'] - merged_df['Adj Close']
    #merged_df['volume_ETH'] = merged_df['amount0In'] + merged_df['amount0Out']

    #merged_df['fee_total'] = merged_df['amount0In'] - merged_df['amount1Out'] * merged_df['spot_price'] + merged_df[
    #    'amount0Out'] - merged_df['amount1In'] * merged_df['spot_price']
    #merged_df['fee'] = merged_df['fee_total'] / merged_df['volume_ETH'] * 100

    return merged_df

# Example usage:
# merged_df = calculate_metrics(merged_df)


def aggregate_data(df, freq):
    agg_dic = dict(MAV='sum', volume_ETH='sum', spot_price='last', price_diff='last', reserves_ETH='last', blockNumber='last', LP_Fee='sum')

    df.set_index('timestamp', inplace=True)
    df_agg = df.resample(freq).agg(agg_dic).dropna(subset=['blockNumber'])

    df_agg['cum_MAV'] = df_agg['MAV'].cumsum()
    df_agg['Return'] = df_agg['LP_Fee'] / df_agg['reserves_ETH']
    df_agg['annual_Return'] = getAnnualReturn(df_agg['Return'])

    return df_agg

# Example usage:
# df_per_minute = aggregate_data(merged_df, 'T')
# df_per_day = aggregate_data(merged_df, 'D')

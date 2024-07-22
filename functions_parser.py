import numpy as np

def process_swap_data(swap_df, CONST_Token0, CONST_Token1):
    swap_df['amount0In'] = np.full(len(swap_df), 0)
    swap_df['amount1In'] = np.full(len(swap_df), 0)
    swap_df['amount0Out'] = np.full(len(swap_df), 0)
    swap_df['amount1Out'] = np.full(len(swap_df), 0)

    swap_df['amount0In'] = swap_df['data'].str[2:66].apply(lambda x: int(x, 16) / CONST_Token0)
    swap_df['amount1In'] = swap_df['data'].str[66:130].apply(lambda x: int(x, 16) / CONST_Token1)
    swap_df['amount0Out'] = swap_df['data'].str[130:194].apply(lambda x: int(x, 16) / CONST_Token0)
    swap_df['amount1Out'] = swap_df['data'].str[194:258].apply(lambda x: int(x, 16) / CONST_Token1)

    # Effective price
    swap_df['price_buy_token0'] = swap_df['amount0In'] / swap_df['amount1Out']
    swap_df['price_buy_token1'] = swap_df['amount0Out'] / swap_df['amount1In']
    swap_df['effective_price'] = swap_df['price_buy_token0'].combine_first(swap_df['price_buy_token1'])

    return swap_df

# Example usage:
# swap_df = process_swap_data(swap_df)

def process_sync_data(sync_df, CONST_Token0, CONST_Token1):
    sync_df['reserve_0'] = np.full(len(sync_df), 0)  # Amount of ETH in the pool
    sync_df['reserve_1'] = np.full(len(sync_df), 0)  # Amount of BTC in the pool

    sync_df['reserve_0'] = sync_df['data'].str[2:66].apply(lambda x: int(x, 16) / CONST_Token0)
    sync_df['reserve_1'] = sync_df['data'].str[66:130].apply(lambda x: int(x, 16) / CONST_Token1)

    # Spot Price BTC/ETH
    sync_df['spot_price'] = sync_df['reserve_0'] / sync_df['reserve_1']

    return sync_df

# yahoo finance 
# https://finance.yahoo.com/quote/AAPL/history/?guccounter=1&guce_referrer=aHR0cHM6Ly9jb2Rlcnpjb2x1bW4uY29tLw&guce_referrer_sig=AQAAAN0-3TXcf8BrXfP_Qx3q_5HrE1hjKZXMfO0f4xUPNSiKZoVPRlbWLjlrAn5gPJ4JScOh3sgpUG_xOTCPWxcbQCL-iM5Kf6JZlC9wjd2Oks0qPFBZ6NOT0ZIHpnZzf3RFP7jyqSFwSj8Z2-tDsy6-IWGkvkbCqzjuXc-ueF8zaWSI


# reference : https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh

from datetime import datetime, timedelta
from matplotlib.pyplot import close
import numpy as np
import mplfinance as fplt

if __name__ == '__main__':
    '''
    '''
    now = datetime.now()
    date = datetime.strptime('20210703', '%Y%m%d')
    if now - timedelta(weeks=4) >= date:
        print('success')
    else:
        print('else')

    import pandas as pd
    apple_df = pd.read_csv('C:\\Users\\KyungHo\\Downloads\\AAPL.csv', index_col=0, parse_dates=True)
    dt_range = pd.date_range(start='2020-08-01', end='2020-08-31')
    apple_df = apple_df[apple_df.index.isin(dt_range)]
    print(apple_df.head())

    print(f'row len #1:{len(apple_df.index)}')
    print(f'row len #2:{apple_df.shape[0]}')
    print(f'col len #2:{apple_df.shape[1]}')

    print(f'first date : {apple_df.index[0]}')
    print(f'first Open : {apple_df["Open"][0]}')
    print(f'first High : {apple_df["High"][0]}')
    print(f'first Low : {apple_df["Low"][0]}')
    print(f'first Close : {apple_df["Close"][0]}')

    i = 5
    dataframe = {
        'Date': apple_df.index[:i],
        'Open': apple_df['Open'][:i],
        'High': apple_df['High'][:i],
        'Low': apple_df['Low'][:i],
        'Close': apple_df['Close'][:i],
    }

    df = pd.DataFrame(dataframe)

    
    fplt.plot(
        df,
        type='candle',
        title='Apple, March - 2020',
        ylabel='Price ($)'
    )


    dates = ['20210702', '20210701', '20210630', '20210629', '20210628', '20210625', '20210624', '20210623', '20210622', '20210621', '20210618', '20210617', '20210616', '20210615']
    opens = ['13900', '14150', '14350', '14500', '14500', '14550', '15100', '15100', '14300', '14700', '14950', '14800', '15100', '15250']
    highes = ['14150', '14300', '14400', '14500', '14700', '14650', '15100', '15400', '15700', '14700', '15000', '14950', '15350', '15400']
    lowes = ['13800', '13800', '14100', '14150', '14200', '14250', '14550', '14850', '14200', '14250', '14550', '14800', '14800', '14950']
    closes = ['14150', '13850', '14250', '14200', '14400', '14500', '14550', '15100', '15100', '14300', '14700', '14900', '14800', '15250']

    dataframe2 = {
        'Open': map(np.float64, reversed(opens)),
        'High': map(np.float64, reversed(highes)),
        'Low': map(np.float64, reversed(lowes)),
        'Close': map(np.float64, reversed(closes)),
    }
    
    
    df2 = pd.DataFrame(dataframe2, pd.to_datetime(dates))

    fplt.plot(
        df2,
        type='candle',
        title='Apple, March - 2020',
        ylabel='Price ($)'
    )

    
    





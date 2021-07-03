

def test1():
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime

    dates = ['01/02/1991', '01/03/1991', '01/04/1991']
    x = [datetime.strptime(d, '%m/%d/%Y').date() for d in dates]
    y = range(len(x))


    


    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(x,y)
    plt.gcf().autofmt_xdate()
    plt.show()

def test2():
    '''
    '''

if __name__ == '__main__':
    '''
    '''
    import mplfinance as mpf
    import pandas_datareader as web

    df = web.naver.NaverDailyReader('005930', start='20201201', end='20210119').read()

    df = df.astype(int)

    colorset = mpf.make_marketcolors(up='tab:red', down='tab:blue', volume='tab:blue')
    s = mpf.make_mpf_style(marketcolors=colorset)
    mpf.plot(df[:60], type='candle', volume=True, style=s)
    # mpf.plot(df, type='candle')




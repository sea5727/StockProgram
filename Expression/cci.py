
import pandas


def search_cci_up(df):
    '''
    '''
    day = 20
    length = len(df)
    ma = df['Close'].rolling(day).mean()
    for i in range(day):
        ma[i] = 0.0
    ma = ma.astype('int64')

    prev_down = False
    for i in range(length):
        if ma[i] < df['Close'][i] and prev_down is True:
            print(f'CCI 기준선 상향 돌파 i:{i}, {df.index[i]}, ma10[{i}]: {ma[i]}, Close: {df["Close"][i]}')
            prev_down = False
            continue
        
        elif ma[i] > df['Close'][i]:
            prev_down = True

def search_cci(df):
    '''
    '''
    day = 20
    length = len(df)

    M = [(df['Close'][i] + df['Low'][i] + df['High'][i])/3 for i in range(length)]
    pM = pandas.Series(M)
    m = pM.rolling(day).mean()
    for i in range(day):
        m[i] = pM[i]
        
    absD = [abs(pM[i] - m[i]) for i in range(length)]
    pabsD = pandas.Series(absD)
    d = pabsD.rolling(day).mean()
    for i in range(day):
        d[i] = d[day+1]

    for i in range(day+day, length, 1):
        cci = (pM[i] - m[i]) / (d[i] * 0.015)
        print(f'CCI 값:{cci} i:{i}, {df.index[i]}')

        


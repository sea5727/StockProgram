
def search_moving(df, day):
    '''
    '''
    #day = 120
    length = len(df)
    ma = df['Close'].rolling(day).mean()
    for i in range(day):
        ma[i] = 0.0
    ma = ma.astype('int64')

    for i in range(day, length, 1):
        if i == day:
            continue
        if i == day+1:
            continue

        if ma[i] > df['Close'][i]:
            print(f'{day}일 이동평균선보다 아래. i:{i}, {df.index[i]}, ma10[{i}]: {ma[i]}, Close: {df["Close"][i]}')
    
    
buy_price = 0
sell_price = 0
total_gap = 0
def trade_point_moving(df):
    '''
    '''
    global buy_price
    global sell_price
    global total_gap

    length = len(df)
    ma5 = df['Close'].rolling(5).mean()
    ma20 = df['Close'].rolling(20).mean()

    hold = False

    for i in range(20, length, 1):
        if ma5[i] > ma20[i] and hold == False:
            buy_price = df["Close"][i]
            print(f'i:{i}, {df.index[i]}, 매수, 현재가격: {buy_price}')
            hold = True
        elif ma5[i] < ma20[i] and hold == True:
            sell_price = df["Close"][i]
            gap = sell_price-buy_price
            total_gap = total_gap + gap
            print(f'i:{i}, {df.index[i]}, 매도, 현재가격: {sell_price}, 차익 : {gap}, 토탈수익:{total_gap}')
            
            hold = False
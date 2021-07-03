
def func1(df):
    print('Hello')
    prev = 0
    for i in range(len(df.index)):
        if prev != 0:
            if prev < df['Open'][i]:
                print(f'{df.index[i]} 매수신호 갭 상승 발생: {df["Open"][i] - prev}')
            elif prev > df['Open'][i]:
                print(f'{df.index[i]} 매도신호 갭 하락 발생: {df["Open"][i] - prev}')
            else:
                '''
                '''
                # print(f'매도신호 갭하락 발생: {df["Open"][i] - prev}')
        
        prev = df['Close'][i]
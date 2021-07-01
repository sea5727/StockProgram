# import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
#matplotlib 패키지 한글 폰트 설정 시작
plt.rcParams["font.family"] = 'Malgun Gothic' #윈도우, 구글 콜랩
#plt.rcParams["font.family"] = 'AppleGothic' #맥
#matplotlib 패키지 한글 폰트 설정 끝

##########데이터 로드

# df_train = pd.DataFrame([
#         ['A01', 2, 1, 60, 139, 'country', 0, 3],
#         ['A02', 3, 2, 80, 148, 'country', 0, 5],
#         ['A03', 3, 4, 50, 149, 'country', 0, 7],
#         ['A04', 5, 5, 40, 151, 'country', 0, 10],
#         ['A05', 7, 5, 35, 154, 'city', 0, 12],
#         ['A06', 2, 5, 45, 149, 'country', 0, 7],
#         ['A07',8, 9, 40, 155, 'city', 1, 13],
#         ['A08', 9, 10, 70, 155, 'city', 3, 13],
#         ['A09', 6, 12, 55, 154, 'city', 0, 12],
#         ['A10', 9, 2, 40, 156, 'city', 1, 13],
#         ['A11', 6, 10, 60, 153, 'city', 0, 12],
#         ['A12', 2, 4, 75, 151, 'country', 0, 6]
#     ], columns=['ID', 'hour', 'attendance', 'weight', 'iq', 'region', 'library', 'score'])

# ##########데이터 분석

# sns.lineplot(x='ID', y='score', data=df_train)
plt.title('선 그래프')
plt.show()
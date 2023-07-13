import pandas as pd
import matplotlib.pyplot as plt
import csv
import folium
import warnings
import platform
from geopy.geocoders import Nominatim

warnings.filterwarnings("ignore")

df = pd.read_csv('./a.csv', encoding='euc-kr')

# 데이터 전처리
# '위치정보' 열에서 '구' 이후의 내용 제거
# df['위치정보'] = df['위치정보'].str.replace('구.*', '', regex=True)
# df['위치정보'] = df['위치정보'].str.replace('(맨홀|\(.*\)).*', '', regex=True)

# 중복된 위치정보를 가진 행 제거
df = df.drop_duplicates(subset='구분명')


# 지오코더 호출
geolocator = Nominatim(user_agent='South Korea')

# 주소를 위도 경도로 변환하여 새로운 열에 추가
df['latitude'] = None
df['longitude'] = None
for i, row in df.iterrows():
    try:
        location = geolocator.geocode(row['구분명']+'구', timeout=None)
        if location is not None:
            df.at[i, 'latitude'] = location.latitude
            df.at[i, 'longitude'] = location.longitude
        else:
            print(f"Unable to geocode address: {row['위치정보']}")
    except Exception as e:
        print(f"Error occurred while geocoding address: {row['위치정보']}")
        print(str(e))

# 새로운 CSV 파일에 저장
df.to_csv('./processed_data.csv', index=False, encoding='euc-kr')

# 데이터 출력
print(1111)
print(df)
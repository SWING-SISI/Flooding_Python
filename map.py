import pandas as pd
import folium
import geopandas as gpd
from branca.colormap import linear

# CSV 파일에서 데이터 읽기
df = pd.read_csv('./processed_data.csv', encoding='euc-kr')

# 대한민국 구 경계 데이터 읽기
gdf = gpd.read_file('./korea_gu.geojson')

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

# 측정수위에 따른 컬러맵 설정
colormap = linear.RdPu_09.scale(df['측정수위'].min(), df['측정수위'].max())

# 각 구에 대한 측정수위에 따른 영역 표시
for _, row in gdf.iterrows():
    gu = row['GU_NM']
    if gu in df['구분명'].values:
        value = df.loc[df['구분명'] == gu, '측정수위'].iloc[0]
        color = colormap(value)
        folium.GeoJson(
            row['geometry'],
            style_function=lambda feature: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            tooltip=gu
        ).add_to(m)

# 컬러맵을 지도에 추가
colormap.add_to(m)

# 지도를 HTML 파일로 저장
m.save('./map.html')

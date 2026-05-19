import streamlit as streamlit
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(
    page_title="서울 주요 관광지 Top 10",
    page_icon="🗺️",
    layout="wide"
)

st.title("외국인이 좋아하는 서울 주요 관광지 Top 10 🗺️")
st.markdown("스트림릿과 폴리움(Folium)을 활용하여 서울의 인기 명소를 소개합니다.")

# 2. 관광지 데이터 정의 (이름, 위도, 경도, 설명)
tourist_spots = [
    {"name": "경복궁", "lat": 37.5796, "lon": 126.9770, "desc": "한국의 전통 미를 느낄 수 있는 대표 고궁"},
    {"name": "N서울타워", "lat": 37.5512, "lon": 126.9882, "desc": "서울 시내를 한눈에 내려다볼 수 있는 야경 명소"},
    {"name": "명동 쇼핑거리", "lat": 37.5635, "lon": 126.9846, "desc": "K-뷰티와 길거리 음식을 즐길 수 있는 쇼핑의 중심지"},
    {"name": "인사동", "lat": 37.5744, "lon": 126.9848, "desc": "한국의 전통 기념품과 전통찻집이 모여있는 곳"},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.5665, "lon": 127.0092, "desc": "독특한 건축물과 트렌디한 전시가 열리는 디자인 복합공간"},
    {"name": "북촌한옥마을", "lat": 37.5829, "lon": 126.9835, "desc": "실제 주민들이 거주하는 아름다운 전통 한옥 밀집 지역"},
    {"name": "홍대거리", "lat": 37.5567, "lon": 126.9235, "desc": "젊음과 인디 문화, 버스킹을 즐길 수 있는 핫플레이스"},
    {"name": "롯데월드타워 & 몰", "lat": 37.5126, "lon": 127.1025, "desc": "세계 5위 높이의 초고층 빌딩과 대형 쇼핑몰"},
    {"name": "이태원 관광특구", "lat": 37.5345, "lon": 126.9943, "desc": "다양한 세계 문화와 이국적인 음식을 만날 수 있는 곳"},
    {"name": "광장시장", "lat": 37.5701, "lon": 127.0010, "desc": "빈대떡, 육회 등 한국의 찐 시장 먹거리를 체험하는 곳"}
]

# 3. 레이아웃 분할 (사이드바 정보창 + 메인 지도창)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📌 명소 리스트")
    # 사이드바 형태로 관광지 선택 기능 추가
    selected_spot = st.selectbox("자세히 보고 싶은 명소를 선택하세요:", [spot["name"] for spot in tourist_spots])
    
    # 선택된 명소의 상세 설명 표시
    for spot in tourist_spots:
        if spot["name"] == selected_spot:
            st.info(f"**{spot['name']}**\n\n{spot['desc']}")
            # 선택된 위치의 위도/경도를 중심으로 지도 재설정하기 위함
            center_lat, center_lon = spot["lat"], spot["lon"]
            zoom_level = 14
            break
else:
    # 선택 안 했을 때 기본 중심지는 서울 시청 부근
    center_lat, center_lon = 37.5665, 126.9780
    zoom_level = 12

with col2:
    st.subheader("🗺️ 지도 확인")
    
    # 4. Folium 지도 생성
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_level)

    # 5. 지도에 마커 추가
    for spot in tourist_spots:
        # 팝업 및 툴팁 설정
        popup = folium.Popup(f"<b>{spot['name']}</b><br>{spot['desc']}", max_width=300)
        tooltip = spot["name"]
        
        # 마커 색상 차별화 (선택된 마커는 빨간색, 나머지는 파란색)
        icon_color = "red" if spot["name"] == selected_spot else "blue"
        
        folium.Marker(
            location=[spot["lat"], spot["lon"]],
            popup=popup,
            tooltip=tooltip,
            icon=folium.Icon(color=icon_color, icon="info-sign")
        ).add_to(m)

    # 6. 스트림릿에 지도 렌더링
    st_folium(m, width="100%", height=500, returned_objects=[])

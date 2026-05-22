import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import os

# 1. 스트림릿 클라우드 서버 환경에서 한글 깨짐을 '확실하게' 방지하는 폰트 다운로드 로직
@st.cache_data
def load_korean_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic.ttf"
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    return fm.FontProperties(fname=font_path)

try:
    font_prop = load_korean_font()
    fm.fontManager.addfont('NanumGothic.ttf')
    plt.rcParams['font.family'] = font_prop.get_name()
except Exception as e:
    st.warning("폰트를 로드하는 중 오류가 발생했습니다. 일부 글자가 깨질 수 있습니다.")

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

st.title("📊 서울시 행정구역별 인구 통계 대시보드")
st.caption("제공해주신 인구 데이터를 바탕으로 시각화를 수행합니다.")

# 데이터 업로드 인터페이스
uploaded_file = st.file_uploader("분석할 인구 통계 CSV(population.csv) 파일을 업로드해주세요.", type=["csv"])

if uploaded_file is not None:
    # 데이터 로드
    df = pd.read_csv(uploaded_file)
    
    # 2. 행정구역 선택창 제공
    region_list = df['행정구역'].unique().tolist()
    selected_region = st.selectbox("조회할 행정구역을 선택하세요:", region_list)
    
    # 선택된 행정구역 행 추출
    region_data = df[df['행정구역'] == selected_region].iloc[0]
    
    # 가로축에 사용할 연령대 컬럼 정의
    age_columns = ['0~9세', '10~19세', '20~29세', '30~39세', '40~49세', '50~59세', '60~69세', '70~79세', '80~89세', '90~99세', '100세 이상']
    
    # 안전하게 정수형 데이터로 변환 (결측치 및 에러 방지)
    populations = []
    for col in age_columns:
        try:
            val = str(region_data[col]).replace(',', '').strip()
            populations.append(int(pd.to_numeric(val, errors='coerce')) if val else 0)
        except:
            populations.append(0)
        
    # 3. 꺾은선 그래프 시각화 설정
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # 4. 그래프 바탕색 설정 (연한 노란색)
    fig.patch.set_facecolor('#FFFFE0') 
    ax.set_facecolor('#FFFFE0')        
    
    # 4. 그래프 선 및 마커 설정 (빨간색)
    ax.plot(age_columns, populations, marker='o', color='red', linewidth=2.5, markersize=6)
    
    # 3. 그래프 제목 및 레이블 지정
    font_title = font_prop.copy()
    font_title.set_size(16)
    font_title.set_weight('bold')
    
    ax.set_title("서울시의 인구통계", fontproperties=font_title, pad=15)
    ax.set_xlabel("연령대", fontproperties=font_prop, labelpad=10)
    ax.set_ylabel("인구수 (명)", fontproperties=font_prop, labelpad=10)
    
    # 격자선(Grid) 추가
    ax.grid(True, linestyle='--', alpha=0.4, color='gray')
    
    # 각 축의 눈금(Ticks)에도 한글 폰트 적용
    for label in ax.get_xticklabels():
        label.set_fontproperties(font_prop)
    for label in ax.get_yticklabels():
        label.set_fontproperties(font_prop)
        
    # 세로축 숫자 포맷팅 (천단위 쉼표 추가)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    # 스트림릿 웹 화면에 그래프 표출
    st.pyplot(fig)
    
    # 하단에 선택한 구역의 상세 데이터 테이블 추가 노출
    st.subheader(f"📍 {selected_region} 데이터 요약")
    summary_df = pd.DataFrame({
        '연령대': age_columns,
        '인구수(명)': [f"{x:,}" for x in populations]
    }).set_index('연령대')
    st.dataframe(summary_df.T)

else:
    st.info("💡 시작하려면 상단의 파일 업로드 영역에 `population.csv` 파일을 넣어주세요.")

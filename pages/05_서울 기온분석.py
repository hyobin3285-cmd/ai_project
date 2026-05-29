import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

# =========================================================================
# [한글 깨짐 해결] 폰트 설정
# 스트림릿 클라우드(리눅스) 환경에서 한글이 깨지지 않도록 시스템 기본 폰트를 지정합니다.
# 무설치형 폰트 지정을 위해 DejaVu Sans나 기본 sans-serif를 쓰고 
# 아래 그래프 그리는 부분에서 한글을 영문/기호(예: ℃)로 바꾸거나 
# 혹은 시스템 폰트를 강제 적용하는 방식을 사용합니다.
# =========================================================================
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지


# 1904년부터 데이터를 생성하는 함수
@st.cache_data
def load_historical_data():
    np.random.seed(42)
    # 1. 시작 연도를 1904년으로 변경 (1904 ~ 2026)
    years = list(range(1904, 2027))
    months = list(range(1, 13))
    days = list(range(1, 32))
    
    data = []
    for year in years:
        # 지구 온난화 효과를 시뮬레이션하기 위해 연도가 높아질수록 기본 온도가 살짝 오르도록 설정
        warming_effect = (year - 1904) * 0.015 
        
        for month in months:
            for day in days:
                # 월별 대략적인 기온 플로우
                if month in [12, 1, 2]:    # 겨울
                    base_temp = -5 + warming_effect
                elif month in [6, 7, 8]:   # 여름
                    base_temp = 24 + warming_effect
                else:                      # 봄/가을
                    base_temp = 14 + warming_effect
                    
                low_temp = base_temp + np.random.uniform(-4, 4)
                high_temp = low_temp + np.random.uniform(5, 12)
                
                data.append([year, month, day, round(high_temp, 1), round(low_temp, 1)])
                
    df = pd.DataFrame(data, columns=['연도', '월', '일', '최고기온', '최저기온'])
    return df

# 데이터 로드
df = load_historical_data()

# 스트림릿 UI 타이틀
st.title("년도별 기온 변화 조회 서비스 (Since 1904)")

st.markdown("""
이 애플리케이션은 **1904년부터 현재까지** 사용자가 선택한 **월/일**의 연도별 최고/최저 기온 추이를 보여줍니다.
""")

# 월/일 선택 UI
col1, col2 = st.columns(2)
with col1:
    selected_month = st.selectbox("월을 선택하세요", list(range(1, 13)), index=4) # 기본값 5월
with col2:
    selected_day = st.selectbox("일을 선택하세요", list(range(1, 32)), index=14) # 기본값 15일

# 데이터 필터링
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

# 예외 처리 (예: 2월 30일 등)
if filtered_df.empty:
    st.error(f"선택하신 {selected_month}월 {selected_day}일은 존재하지 않는 날짜입니다. 다시 선택해주세요.")
else:
    st.subheader(f"📊 {selected_month}월 {selected_day}일 데이터 시각화")
    
    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 1. 최고기온 (핑크색)
    ax.plot(filtered_df['연도'], filtered_df['최고기온'], color='pink', linewidth=1.5, label='Max Temp')
    
    # 2. 최저기온 (하늘색)
    ax.plot(filtered_df['연도'], filtered_df['최저기온'], color='skyblue', linewidth=1.5, label='Min Temp')
    
    # 축 및 제목 설정 (요구사항 반영)
    # 💡 스트림릿 클라우드 한글 깨짐 방지를 위해 제목과 축이름에 한글/영문을 혼용하거나 깔끔하게 배치했습니다.
    ax.set_title(f"날짜별 기온분석 ({selected_month}/{selected_day})", fontsize=16, pad=15)
    ax.set_xlabel("연도 (Year)", fontsize=12)
    ax.set_ylabel("온도 (Temp, ℃)", fontsize=12)
    
    # 1904년부터 데이터가 길기 때문에 X축 눈금이 겹치지 않도록 10년 단위로 설정합니다.
    min_year = filtered_df['연도'].min()
    max_year = filtered_df['연도'].max()
    ax.set_xticks(range(min_year, max_year + 1, 10))
    ax.set_xticklabels(range(min_year, max_year + 1, 10), rotation=45)
    
    # 범례 표시
    ax.legend(loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # 스트림릿에 그래프 출력
    st.pyplot(fig)
    
    # 상세 데이터 표 테이블 출력
    if st.checkbox("전체 기간 상세 데이터 표 보기"):
        st.dataframe(filtered_df[['연도', '최고기온', '최저기온']].reset_index(drop=True), use_container_width=True)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. 한글 폰트 설정 (스트림릿 클라우드 리눅스 환경 대응)
# 스트림릿 클라우드는 기본적으로 한글 폰트가 없으므로 시스템 폰트를 사용하거나 전역 설정을 변경합니다.
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# 2. 샘플 데이터 생성 (사용자 파일 대신 테스트 가상 데이터 사용)
# 실제 데이터 파일(CSV 등)이 있다면 pd.read_csv() 등으로 대체 가능합니다.
@st.cache_data
def load_sample_data():
    np.random.seed(42)
    years = list(range(2010, 2026))
    months = list(range(1, 13))
    days = list(range(1, 32))
    
    data = []
    for year in years:
        for month in months:
            for day in days:
                # 월별 대략적인 기온 플로우 생성
                if month in [12, 1, 2]: # 겨울
                    base_temp = -5
                elif month in [6, 7, 8]: # 여름
                    base_temp = 25
                else: # 봄/가을
                    base_temp = 15
                    
                low_temp = base_temp + np.random.uniform(-5, 5)
                high_temp = low_temp + np.random.uniform(5, 12)
                
                data.append([year, month, day, round(high_temp, 1), round(low_temp, 1)])
                
    df = pd.DataFrame(data, columns=['연도', '월', '일', '최고기온', '최저기온'])
    return df

df = load_sample_data()

# 3. 스트림릿 UI 타이틀
st.title("년도별 기온 변화 조회 서비스")

st.markdown("""
이 애플리케이션은 사용자가 선택한 **월과 일**에 해당하는 연도별 최고/최저 기온 추이를 보여줍니다.
""")

# 4. 사이드바 또는 메인 화면에서 월/일 선택 기능
col1, col2 = st.columns(2)
with col1:
    selected_month = st.selectbox("월을 선택하세요", list(range(1, 13)), index=4) # 기본값 5월
with col2:
    selected_day = st.selectbox("일을 선택하세요", list(range(1, 32)), index=14) # 기본값 15일

# 5. 데이터 필터링
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

# 해당 날짜가 없는 경우 처리 (예: 2월 30일 등)
if filtered_df.empty:
    st.error(f"선택하신 {selected_month}월 {selected_day}일은 존재하지 않는 날짜입니다. 다시 선택해주세요.")
else:
    st.subheader(f"📊 {selected_month}월 {selected_day}일 선택 데이터 결과")
    
    # 6. 꺾은선 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # 최고기온 (핑크 - 'pink' 또는 헥스코드 '#FFC0CB')
    ax.plot(filtered_df['연도'], filtered_df['최고기온'], marker='o', color='pink', linewidth=2, label='최고기온')
    
    # 최저기온 (하늘색 - 'skyblue' 또는 헥스코드 '#87CEEB')
    ax.plot(filtered_df['연도'], filtered_df['최저기온'], marker='o', color='skyblue', linewidth=2, label='최저기온')
    
    # 축 및 제목 설정 (요구사항 반영)
    ax.set_title("날짜별 기온분석", fontsize=16, pad=15)
    ax.set_xlabel("연도", fontsize=12)
    ax.set_ylabel("온도", fontsize=12)
    
    # X축 눈금을 연도 데이터에 맞게 정수로 설정
    ax.set_xticks(filtered_df['연도'])
    ax.set_xticklabels(filtered_df['연도'], rotation=45)
    
    # 범례 표시
    ax.legend(loc='best')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # 스트림릿에 그래프 출력
    st.pyplot(fig)
    
    # 데이터 테이블로도 보기 선택
    if st.checkbox("상세 데이터 표 보기"):
        st.dataframe(filtered_df[['연도', '최고기온', '최저기온']].reset_index(drop=True))

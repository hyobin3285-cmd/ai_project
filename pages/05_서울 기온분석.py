import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# ==========================================
# 1. 역사적 데이터 생성 (1904 ~ 2026년)
# ==========================================
@st.cache_data
def load_historical_data():
    np.random.seed(42)
    years = list(range(1904, 2027)) # 2026년까지 실제 데이터가 있다고 가정
    months = list(range(1, 13))
    days = list(range(1, 32))
    
    data = []
    for year in years:
        # 지구 온난화 효과 반영 (과거에서 현재로 올수록 기온이 완만하게 상승)
        warming_effect = (year - 1904) * 0.015 
        
        for month in months:
            for day in days:
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

df = load_historical_data()

# ==========================================
# 2. 스트림릿 UI 구성
# ==========================================
st.title("년도별 기온 분석 및 미래 예측 서비스")

st.markdown("""
마우스를 그래프 위에 올리면 **정확한 연도와 기온**을 확인할 수 있습니다.  
미래의 연도를 선택하시면 과거 추세를 분석하여 기온을 예측해 드립니다.
""")

# 월/일 선택 UI
col1, col2 = st.columns(2)
with col1:
    selected_month = st.selectbox("월을 선택하세요", list(range(1, 13)), index=4) # 기본값 5월
with col2:
    selected_day = st.selectbox("일을 선택하세요", list(range(1, 32)), index=14) # 기본값 15일

# 선택한 날짜 데이터 필터링 (1904 ~ 2026)
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

if filtered_df.empty:
    st.error(f"선택하신 {selected_month}월 {selected_day}일은 존재하지 않는 날짜입니다. 다시 선택해주세요.")
else:
    st.subheader(f"📊 {selected_month}월 {selected_day}일 날짜별 기온분석")
    
    # ==========================================
    # 3. 미래 연도 선택 및 예측 기능 (머신러닝)
    # ==========================================
    st.sidebar.header("🔮 미래 기온 예측 설정")
    target_year = st.sidebar.number_input(
        "예측하고 싶은 미래 연도를 입력하세요", 
        min_value=2027, 
        max_value=2100, 
        value=2030, 
        step=1
    )
    
    # 사이드바 예측 실행 버튼
    if st.sidebar.button("미래 기온 예측하기"):
        X = filtered_df[['연도']].values
        y_high = filtered_df['최고기온'].values
        y_low = filtered_df['최저기온'].values
        
        # 최고기온 모델 학습 및 예측
        model_high = LinearRegression().fit(X, y_high)
        pred_high = model_high.predict([[target_year]])[0]
        
        # 최저기온 모델 학습 및 예측
        model_low = LinearRegression().fit(X, y_low)
        pred_low = model_low.predict([[target_year]])[0]
        
        # 결과 출력
        st.sidebar.success(f"### 🎯 {target_year}년 {selected_month}월 {selected_day}일 예측 결과")
        st.sidebar.metric(label="예측 최고기온", value=f"{pred_high:.1f} ℃")
        st.sidebar.metric(label="예측 최저기온", value=f"{pred_low:.1f} ℃")
        
        # 예측 데이터를 기존 데이터프레임에 결합하여 그래프에 표시
        pred_row = pd.DataFrame({
            '연도': [target_year], '월': [selected_month], '일': [selected_day],
            '최고기온': [round(pred_high, 1)], '최저기온': [round(pred_low, 1)]
        })
        plot_df = pd.concat([filtered_df, pred_row]).sort_values('연도')
    else:
        plot_df = filtered_df

    # ==========================================
    # 4. Plotly 인터랙티브 꺾은선 그래프
    # ==========================================
    fig = go.Figure()
    
    # 최고기온 선 (핑크)
    fig.add_trace(go.Scatter(
        x=plot_df['연도'], 
        y=plot_df['최고기온'],
        mode='lines+markers',
        name='최고기온',
        line=dict(color='pink', width=2),
        marker=dict(size=6),
        hovertemplate='<b>연도</b>: %{x}년<br><b>최고기온</b>: %{y}°C<extra></extra>'
    ))
    
    # 최저기온 선 (하늘색)
    fig.add_trace(go.Scatter(
        x=plot_df['연도'], 
        y=plot_df['최저기온'],
        mode='lines+markers',
        name='최저기온',
        line=dict(color='skyblue', width=2),
        marker=dict(size=6),
        hovertemplate='<b>연도</b>: %{x}년<br><b>최저기온</b>: %{y}°C<extra></extra>'
    ))
    
    # 레이아웃 및 축 설정
    fig.update_layout(
        title=dict(text="날짜별 기온분석", x=0.5, font=dict(size=18)),
        xaxis=dict(title="연도", tickmode='linear', dtick=10, tickangle=45),
        yaxis=dict(title="온도"),
        hovermode="x unified", 
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=80, b=40),
        template="plotly_white"
    )
    
    # 스트림릿 웹 화면에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)
    
    # 데이터 테이블 보기
    if st.checkbox("데이터 표 형태로 보기"):
        st.dataframe(plot_df[['연도', '최고기온', '최저기온']].reset_index(drop=True), use_container_width=True)

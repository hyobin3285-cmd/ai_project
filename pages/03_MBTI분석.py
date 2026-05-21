import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="Global MBTI Distribution Dashboard", layout="wide")

st.title("🌍 전 세계 국가별 MBTI 분포 대시보드")
st.markdown("공공 또는 연구용 MBTI 데이터셋을 기반으로 국가별 성격 유형 비율을 시각화합니다.")

# 데이터 로드
@st.cache_data
def load_data():
    try:
        # 업로드한 파일 이름을 그대로 불러옵니다.
        df = pd.read_csv('countriesMBTI_16types.csv')
        return df
    except FileNotFoundError:
        st.error("데이터 파일('countriesMBTI_16types.csv')을 찾을 수 없습니다. GitHub 저장소에 파일이 함께 있는지 확인해주세요.")
        return None

df = load_data()

if df is not None:
    # 사이드바에서 국가 선택
    countries = sorted(df['Country'].unique())
    selected_country = st.sidebar.selectbox("📊 분석할 국가를 선택하세요:", countries)

    # 선택된 국가의 데이터 추출
    country_data = df[df['Country'] == selected_country].iloc[0]
    
    # MBTI 유형과 비율 추출 (Country 열 제외)
    mbti_types = df.columns[1:]
    percentages = [country_data[mbti] * 100 for mbti in mbti_types]  # 백분율(%)로 변환

    # 데이터프레임으로 변환 후 비율이 높은 순서대로 정렬
    plot_df = pd.DataFrame({
        'MBTI': mbti_types,
        'Percentage': percentages
    }).sort_values(by='Percentage', ascending=False).reset_index(drop=True)

    # 1등 및 나머지 색상 계산 (1등: 빨간색, 나머지: 파란색 그라데이션)
    colors = []
    n_items = len(plot_df)
    
    for i in range(n_items):
        if i == 0:
            # 1등: 세련되고 명확한 고급스러운 빨간색
            colors.append('#D32F2F')
        else:
            # 나머지: 순위가 내려갈수록(비율이 낮아질수록) 점차 연해지는 파란색 그라데이션
            alpha = 1.0 - (i / n_items) * 0.6  # 최소 투명도 0.4까지 조절
            colors.append(f'rgba(41, 128, 185, {alpha})')

    # 플로틀리(Plotly) 인터랙티브 막대그래프 구성
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=plot_df['MBTI'],
        y=plot_df['Percentage'],
        marker_color=colors,
        text=[f"{val:.2f}%" for val in plot_df['Percentage']],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>비율: %{y:.2f}%<extra></extra>',
    ))

    # 차트 레이아웃 스타일링
    fig.update_layout(
        title=f"📊 {selected_country}의 MBTI 성격 유형 분포 (1위 강조)",
        xaxis_title="MBTI 유형",
        yaxis_title="비율 (%)",
        yaxis=dict(ticksuffix="%"),
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200, 200, 200, 0.3)')

    # 화면 레이아웃 분할 (좌측: 그래프, 우측: 주요 요약 정보 카드)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader(f"💡 {selected_country} 요약 정보")
        top_1 = plot_df.iloc[0]
        top_2 = plot_df.iloc[1]
        top_3 = plot_df.iloc[2]
        
        st.metric(label="🥇 가장 많은 유형 (1위)", value=f"{top_1['MBTI']}", delta=f"{top_1['Percentage']:.2f}%")
        st.metric(label="🥈 2위 유형", value=f"{top_2['MBTI']}", delta=f"{top_2['Percentage']:.2f}%")
        st.metric(label="🥉 3위 유형", value=f"{top_3['MBTI']}", delta=f"{top_3['Percentage']:.2f}%")
        
        with st.expander("전체 비율 데이터 테이블 보기"):
            st.dataframe(plot_df.style.format({'Percentage': '{:.2f}%'}), use_container_width=True)

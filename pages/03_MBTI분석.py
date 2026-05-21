import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="글로벌 MBTI 분석기", layout="wide")

st.title("🌍 전 세계 MBTI 분포 분석 대시보드")
st.markdown("특정 MBTI 유형을 선택하면, 해당 유형의 비율이 가장 높은 **상위 10개국**을 보여줍니다.")

# 2. 데이터 로드 (캐싱을 통해 속도 향상)
@st.cache_data
def load_data():
    # 데이터 파일 읽기 (동일 경로에 있다고 가정)
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()
    
    # MBTI 컬럼 목록 가져오기 (Country 제외)
    mbti_columns = [col for col in df.columns if col != 'Country']

    # 3. 사이드바 - MBTI 유형 선택
    selected_mbti = st.sidebar.selectbox(
        "🧐 궁금한 MBTI 유형을 선택하세요:",
        options=sorted(mbti_columns)
    )

    # 4. 데이터 가공: 선택한 MBTI 기준 상위 10개국 추출
    # 퍼센트 표시를 위해 100을 곱해줍니다.
    df_filtered = df[['Country', selected_mbti]].copy()
    df_filtered[selected_mbti] = df_filtered[selected_mbti] * 100
    
    # 상위 10개국 정렬 (내림차순)
    top10 = df_filtered.sort_values(by=selected_mbti, ascending=False).head(10)
    
    # 그래프 순서를 위해 역순 정렬 (Plotly 세로 막대그래프는 위에서부터 그리므로 정렬 유지)
    top10 = top10.iloc[::-1]

    # 5. 시각화 (Plotly)
    # 1등은 빨간색, 나머지는 파란색 그라데이션을 표현하기 위해 커스텀 컬러 순서 생성
    # 가장 높은 값(1등)이 그라데이션의 끝(빨간색)에 오도록 매핑합니다.
    # Plotly Continuous Color에서는 값의 스케일에 따라 색이 바뀝니다.
    
    # 커스텀 컬러 스케일 정의: 0(최저) ~ 0.8까지는 파란색 그라데이션, 1.0(최고)은 빨간색
    custom_colors = [
        [0.0, "#d1e5f0"],  # 연한 파랑
        [0.8, "#045a8d"],  # 진한 파랑 (2등 수준)
        [1.0, "#d73027"]   # 빨간색 (1등)
    ]

    fig = px.bar(
        top10,
        x=selected_mbti,
        y='Country',
        orientation='h',  # 가로 막대 그래프가 가독성이 좋습니다
        title=f"🏆 {selected_mbti} 비율이 가장 높은 국가 Top 10",
        labels={selected_mbti: "비율 (%)", "Country": "국가"},
        color=selected_mbti,
        color_continuous_scale=custom_colors,
        text_auto='.2f'  # 막대 위에 소수점 둘째 자리까지 표시
    )

    # 레이아웃 깔끔하게 다듬기
    fig.update_layout(
        plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#eeeeee"),
        yaxis=dict(autorange="reversed"), # 1등이 맨 위로 오도록 설정
        coloraxis_showscale=False, # 컬러바 숨기기 (깔끔함 유지)
        title_font_size=20,
        height=500
    )
    
    fig.update_traces(
        textposition="outside", 
        cliponaxis=False
    )

    # 6. 스트림릿 화면에 출력
    st.plotly_chart(fig, use_container_width=True)
    
    # 데이터 테이블도 하단에 깔끔하게 보여주기
    st.markdown("### 📊 상세 데이터 테이블")
    st.dataframe(
        top10.iloc[::-1].rename(columns={selected_mbti: f"{selected_mbti} 비율 (%)"}),
        use_container_width=True,
        hide_index=True
    )

except FileNotFoundError:
    st.error("❌ `countriesMBTI_16types.csv` 파일을 찾을 수 없습니다. 코드와 같은 폴더에 넣어주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")

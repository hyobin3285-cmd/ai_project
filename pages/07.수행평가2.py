import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="내 손안의 무알콜 바 🍸", page_icon="🍹")

# 앱 제목과 인사
st.title("🍹 오늘 너에게 딱 맞는 '무알콜 칵테일' 추천!")
st.subheader("안녕! 지금 기분은 어때? 그리고 같이 먹을 음식은 뭐야? 기가 막힌 조합을 찾아줄게! ✨")

# 입력 섹션
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        mood = st.selectbox(
            "오늘 너의 기분은? 😊",
            ["신나고 에너제틱해! 🔥", "조금 지치고 힐링이 필요해 🌿", "차분하게 집중하고 싶어 📖", "달달한 게 땡기는 기분이야 🍭", "답답해서 리프레시가 필요해 🌊"]
        )
    
    with col2:
        food = st.text_input("오늘의 메인 메뉴는 뭐야? 🍕", placeholder="예: 피자, 스테이크, 샐러드 등")

# 추천 로직 (간단하지만 센스 있게!)
if st.button("나를 위한 추천 칵테일 보기! 🚀"):
    if not food:
        st.warning("메뉴를 알려주면 더 맛있는 조합을 추천해줄 수 있어! 🥘")
    else:
        st.divider()
        st.balloons() # 축하 효과!
        
        # 기분에 따른 추천 칵테일 데이터
        recommendations = {
            "신나고 에너제틱해! 🔥": {
                "name": "버진 모히토 (Virgin Mojito) 🍃",
                "desc": "라임의 상큼함과 애플민트의 청량함이 너의 텐션을 더 업시켜줄 거야!",
                "pairing": f"에너지 넘치는 기분에는 {food}랑 이보다 더 잘 어울릴 수 없지!"
            },
            "조금 지치고 힐링이 필요해 🌿": {
                "name": "선라이즈 펀치 (Sunrise Punch) 🌅",
                "desc": "오렌지와 그레나딘 시럽의 따뜻한 색감이 너의 마음을 포근하게 감싸줄 거야.",
                "pairing": f"지친 하루 끝에 먹는 {food}, 그리고 이 달콤한 칵테일로 힐링해봐."
            },
            "차분하게 집중하고 싶어 📖": {
                "name": "애플 스파클러 (Apple Sparkler) 🍎",
                "desc": "깔끔한 사과향과 은은한 탄산이 너의 생각을 맑게 정리해줄 거야.",
                "pairing": f"담백한 {food}와 깔끔한 애플 스파클러는 환상의 짝꿍이야."
            },
            "달달한 게 땡기는 기분이야 🍭": {
                "name": "버진 피나콜라다 (Virgin Piña Colada) 🥥",
                "desc": "코코넛의 부드러움과 파인애플의 달콤함이 입안 가득 행복을 줄 거야!",
                "pairing": f"{food} 먹고 나서 이 달콤함으로 마무리하면 최고지!"
            },
            "답답해서 리프레시가 필요해 🌊": {
                "name": "블루 레몬 에이드 (Blue Lemonade) 💎",
                "desc": "보기만 해도 시원해지는 푸른색과 톡 쏘는 레몬이 가슴을 뻥 뚫어줄 거야.",
                "pairing": f"답답함은 잊어버려! {food}와 시원한 블루 레몬 에이드가 있잖아."
            }
        }
        
        result = recommendations[mood]
        
        # 결과 출력
        st.success(f"### 짜잔! 오늘의 추천은 **{result['name']}**")
        st.write(f"✨ **어떤 맛인가요?** {result['desc']}")
        st.write(f"🍴 **꿀조합 포인트:** {result['pairing']}")
        
        st.info("💡 **Tip:** 무알콜이라 언제든 가볍게 즐길 수 있어! 맛있게 먹어! 맛점/맛저! 😋")

# 하단 푸터
st.markdown("---")
st.caption("Made with ❤️ by Your AI Bartender")

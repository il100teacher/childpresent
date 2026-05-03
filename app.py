import streamlit as st
from openai import OpenAI

# 🔐 Secrets에서 불러오기
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
MY_PARTNER_TAG = st.secrets["COUPANG_PARTNER_TAG"]

client = OpenAI(api_key=OPENAI_API_KEY)


def get_ai_letter(name, gender, age, interest, length_option):
    length_map = {
        "단문": "어린이날 한 문장의 짧고 강렬한 카톡 메시지 스타일",
        "중문": "어린이날 3~4문장의 다정한 카드 문구 스타일",
        "장문": "어린이날 진심이 담긴 4문장의 어린이 시선에서 편지 스타일"
    }

    prompt = f"""
    어린이날을 맞아 {age} {gender} 아이 '{name}'에게 보낼 축하 메시지를 작성해줘.
    아이의 관심사는 '{interest}'이야.
    글의 길이는 {length_map[length_option]}로 작성해주고,
    아이의 눈높이에 맞춰서 다정하게 작성해줘.
    마지막엔 사랑한다는 표현을 꼭 넣어줘.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def get_products(keyword):
    search_url = f"https://www.coupang.com/np/search?q={keyword}"

    return [
        {
            "name": f"🎁 {keyword} 인기 세트",
            "price": "확인 필요",
            "link": f"{search_url}&lptag={MY_PARTNER_TAG}"
        },
        {
            "name": f"🔥 {keyword} 베스트 상품",
            "price": "최저가 보장",
            "link": f"{search_url}&lptag={MY_PARTNER_TAG}"
        }
    ]


st.set_page_config(page_title="어린이날 AI 편지 비서", page_icon="💌")
st.title("💌 우리 아이 맞춤형 AI 편지 & 선물")

with st.container():
    name = st.text_input("아이 이름", "사랑하는 아들")

    col1, col2 = st.columns(2)

    with col1:
        gender = st.radio("성별", ["남아", "여아"], horizontal=True)
        age = st.selectbox(
            "나이",
            ["영유아", "유치원생", "초등 저학년", "초등 고학년"],
            index=1
        )

    with col2:
        interest = st.text_input("관심사", "게임")
        length = st.select_slider(
            "편지 길이",
            options=["단문", "중문", "장문"],
            value="중문"
        )


if st.button("✨ 어린이날 메세지 작성하기"):
    with st.spinner("AI가 편지를 작성 중입니다..."):
        letter = get_ai_letter(name, gender, age, interest, length)

        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 25px; border-radius: 15px;">
            <h4>💝 {name} 어린이날 편지</h4>
            <p>{letter.replace('\n', '<br>')}</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.subheader(f"🎁 {interest} 추천 선물")

        # 선물 리스트 출력
        for p in get_products(interest):
            col1, col2 = st.columns([4,1])
            with col1:
                st.write(f"**{p['name']}**")
                st.caption(p['price'])
            with col2:
                st.link_button("보기", p['link'])
        
        # 📢 공정위 문구 추가 (선물 리스트 하단)
        st.caption("이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.")

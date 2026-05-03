import streamlit as st
from openai import OpenAI  # 최신 버전 호출 방식
import requests
from bs4 import BeautifulSoup


# --- [설정] 본인의 API 키와 파트너스 ID를 넣으세요 ---
OPENAI_API_KEY = "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"
MY_PARTNER_TAG = "AF2324136" 

# 최신 방식의 클라이언트 생성
client = OpenAI(api_key=OPENAI_API_KEY)

# AI 편지 생성 함수 (최신 v1.0+ API 적용)
def get_ai_letter(name, gender, age, interest, length_option):
    length_map = {
        "단문": "어린이날 한 문장의 짧고 강렬한 카톡 메시지 스타일",
        "중문": "어린이날 3~4문장의 다정한 카드 문구 스타일",
        "장문": "어린이날 진심이 담긴 4문장의 어린이 시선에서 편지 스타일"
    }
    
    prompt = f"""
    어린이날을 맞아 {age} {gender} 아이 '{name}'에게 보낼 축하 메시지를 작성해줘.
    아이의 관심사는 '{interest}'이야.
    글의 길이는 {length_map[length_option]}로 작성해주고, 아이의 눈높이에 맞춰서 다정하게 작성해줘.
    마지막엔 사랑한다는 표현을 꼭 넣어줘.
    """
    
    try:
        # 최신 API 호출 방식
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 메시지 생성 중 오류가 발생했습니다: {e}"

# 선물 리스트 가져오기 (쿠팡 검색 기반)
def get_products(keyword):
    # 실제 상품 이미지와 가격을 보여주기 위한 기본 구조
    # (실제 운영시에는 더 정교한 크롤링이나 쿠팡 API 사용 권장)
    search_url = f"https://www.coupang.com/np/search?q={keyword}"
    return [
        {"name": f"🎁 {keyword} 인기 세트", "price": "확인 필요", "link": f"{search_url}&lptag={MY_PARTNER_TAG}"},
        {"name": f"🔥 {keyword} 베스트 상품", "price": "최저가 보장", "link": f"{search_url}&lptag={MY_PARTNER_TAG}"}
    ]

# --- 웹 UI 구성 ---
st.set_page_config(page_title="어린이날 AI 편지 비서", page_icon="💌")
st.title("💌 우리 아이 맞춤형 AI 편지 & 선물")
st.write("아이의 정보를 입력하면 AI가 감동적인 편지를 쓰고 선물을 추천해드립니다.")

# 입력 폼
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
        interest = st.text_input("관심사 (예: 게임, 축구, 로봇, 노래 등)", "게임")
        length = st.select_slider(
                                        "편지 길이",
                                        options=["단문", "중문", "장문"],
                                        value="중문"
                                    )

if st.button("✨ 1초 만에 결과 확인하기"):
    if not OPENAI_API_KEY or "OpenAI_API_키" in OPENAI_API_KEY:
        st.error("OpenAI API 키를 먼저 입력해 주세요!")
    else:
        with st.spinner('AI가 정성껏 편지를 작성하고 있습니다...'):
            # 1. AI 편지 생성
            letter = get_ai_letter(name, gender, age, interest, length)
            
            # 2. 결과 카드 디자인
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 25px; border-radius: 15px; border-left: 5px solid #ff4b4b;">
                <h4 style="margin-top:0;">💝 {name}를 위한 특별한 편지</h4>
                <p style="font-size: 16px; line-height: 1.6;">{letter.replace('\n', '<br>')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 3. 선물 리스트 노출
            st.divider()
            st.subheader(f"🎁 {interest} 관련 추천 선물 리스트")
            products = get_products(interest)
            
            for p in products:
                col_info, col_btn = st.columns([4, 1])
                with col_info:
                    st.write(f"**{p['name']}**")
                    st.caption(f"가격대: {p['price']}")
                with col_btn:
                    st.link_button("선물보기", p['link'])
            
            st.divider()
            st.caption("※ 파트너스 활동의 일환으로 일정액의 수수료를 제공받을 수 있습니다.")

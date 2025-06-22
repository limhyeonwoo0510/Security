import pandas as pd
import matplotlib as plt
import streamlit as st
from streamlit_option_menu import option_menu
from utils import search_naver_news
from utils import draw_bar_chart

# 앱 설정
st.set_page_config(page_title="보안 교육 웹앱", layout="centered")

# 사이드바 메뉴
with st.sidebar:
    selected = option_menu(
        menu_title="보안 웹페이지",
        options=["보안이란?", "보안 관련 뉴스", "보안 자가진단"],
        icons=["shield-lock", "newspaper", "clipboard-check"],
        menu_icon="cast",
        default_index=0,
    )

# 페이지 1: 보안이란?
if selected == "보안이란?":
    df = pd.read_csv("경찰청_연도별 사이버 범죄 통계 현황_20200831.csv", encoding="cp949")
    df_occurrence = df[df["구분"] == "발생건수"]
    
    # 필요한 열만 선택
    columns_to_plot = [
        "연도",
        "해킹(계정도용)",
        "해킹(단순침입)",
        "해킹(자료유출)",
        "해킹(자료훼손)",
        "악성프로그램(랜섬웨어)",
        "악성프로그램(기타)",
    ]
    df_chart = df_occurrence[columns_to_plot].sort_values("연도")
    
    st.title("🔐 보안이란 무엇인가?")
    st.markdown("""
    보안(Security)은 정보 자산을 외부의 위협으로부터 안전하게 보호하는 활동입니다.

    - **기밀성(Confidentiality)**: 허가되지 않은 접근으로부터 정보를 보호합니다.
    - **무결성(Integrity)**: 정보가 변경되거나 손상되지 않도록 합니다.
    - **가용성(Availability)**: 정당한 사용자가 언제든 정보에 접근할 수 있도록 보장합니다.

    정보 보안은 일상생활의 필수 요소이며, 안전한 비밀번호 사용, 보안 소프트웨어 설치, 2단계 인증 등이 중요합니다.
    """)
    
    st.subheader("📊 연도별 사이버 범죄 발생 추이")
    fig = draw_bar_chart(df_chart)
    st.pyplot(fig)
    
    st.markdown("""
    #### 보안 범죄 증가 추세
    최근 몇 년간 해킹과 악성 프로그램을 통한 사이버 범죄가 꾸준히 증가하고 있습니다.  
    이는 디지털 환경이 발전하면서 보안 위협도 함께 커지고 있음을 보여줍니다.

    #### 개인이 지켜야 할 예방 방법
    - **강력하고 복잡한 비밀번호 사용**: 숫자, 특수문자, 대문자, 소문자를 혼합해서 만드세요.
    - **주기적인 비밀번호 변경**: 같은 비밀번호를 오래 사용하지 마세요.
    - **2단계 인증(2FA) 활성화**: 가능하면 모든 서비스에 적용하세요.
    - **의심스러운 링크 클릭 금지**: 알 수 없는 출처의 이메일이나 메시지는 조심하세요.
    - **보안 소프트웨어 업데이트 유지**: 항상 최신 버전을 사용해 취약점을 막으세요.

    꾸준한 보안 습관으로 사이버 범죄로부터 스스로를 보호할 수 있습니다.
    """)

# 페이지 2: 보안 관련 뉴스
elif selected == "보안 관련 뉴스":
    st.title("📰 보안 관련 뉴스")
    st.write("네이버 뉴스에서 ‘보안’ 관련 실시간 뉴스를 검색합니다.")
    
    query = st.text_input("🔍 검색어를 입력하세요", value="보안")
    num = st.slider("표시할 뉴스 개수", 1, 10, 5)

    if st.button("뉴스 검색"):
        with st.spinner("뉴스를 검색 중입니다..."):
            news_list = search_naver_news(query=query, num_results=num)

        if news_list:
            for news in news_list:
                st.markdown(f"🔗 [{news['title']}]({news['link']})")
        else:
            st.warning("검색 결과가 없습니다.")

# 페이지 3: 보안 자가진단
elif selected == "보안 자가진단":
    st.title("📝 보안 자가진단")
    st.markdown("아래 항목에 대해 스스로 점검해보세요.")

    score = 0

    if st.checkbox("✔️ 비밀번호에 숫자, 특수문자, 대소문자를 혼합하여 사용한다."):
        score += 1
    if st.checkbox("✔️ 2단계 인증(2FA)을 사용한다."):
        score += 1
    if st.checkbox("✔️ 공용 Wi-Fi 사용 시 VPN을 이용한다."):
        score += 1
    if st.checkbox("✔️ 의심스러운 링크는 클릭하지 않는다."):
        score += 1
    if st.checkbox("✔️ 보안 소프트웨어를 설치하고 항상 최신 상태로 유지한다."):
        score += 1

    if st.button("결과 보기"):
        st.subheader("🧾 진단 결과")
        st.write(f"보안 점수: {score} / 5")

        if score == 5:
            st.success("✅ 훌륭합니다! 보안 인식이 매우 높습니다.")
        elif score >= 3:
            st.info("ℹ️ 괜찮습니다. 하지만 몇 가지 주의할 점이 있어요.")
        else:
            st.warning("⚠️ 보안 위험이 존재합니다. 조치를 취하세요!")

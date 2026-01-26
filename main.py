import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="용인시 통합 정보 서비스",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 메뉴 스타일 개선
st.markdown("""
<style>
    /* 사이드바 메뉴 글자 크기 및 스타일 */
    [data-testid="stSidebarNav"] {
        background-color: #f8f9fa;
        padding-top: 2rem;
    }
    
    [data-testid="stSidebarNav"] li {
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSidebarNav"] a {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 1rem !important;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        background-color: #e9ecef !important;
        transform: translateX(5px);
    }
    
    [data-testid="stSidebarNav"] a span {
        color: #212529 !important;
    }
    
    /* 선택된 메뉴 강조 */
    [data-testid="stSidebarNav"] li a[aria-current="page"] {
        background-color: #667eea !important;
        color: white !important;
    }
    
    [data-testid="stSidebarNav"] li a[aria-current="page"] span {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.title("🏙️ 글로리요의 맛집 정보 서비스")
st.markdown("---")

# 소개 섹션
st.markdown("""
<div style="text-align: center; padding: 50px 0;">
    <h2>용인시에서 가본 맛집 정보와 와이페이 가맹점 정보를 한 곳에서!</h2>
    <p style="font-size: 18px; color: #666; margin-top: 20px;">
        왼쪽 사이드바에서 원하는 서비스를 선택하세요
    </p>
</div>
""", unsafe_allow_html=True)

# 서비스 소개 카드
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin: 10px;
    ">
        <h3>🍴 맛집 검색</h3>
        <p style="font-size: 16px; margin-top: 15px;">
            용인시 기흥구, 수지구, 처인구의<br>
            다양한 맛집 정보를 검색하고<br>
            지도에서 위치를 확인하세요!
        </p>
        <ul style="margin-top: 15px; font-size: 14px;">
            <li>지역별, 카테고리별 검색</li>
            <li>가격대 및 주소 정보</li>
            <li>네이버/카카오/구글 지도 연동</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin: 10px;
    ">
        <h3>💳 와이페이 가맹점</h3>
        <p style="font-size: 16px; margin-top: 15px;">
            용인시 와이페이카드를<br>
            사용할 수 있는 가맹점을<br>
            검색하고 확인하세요!
        </p>
        <ul style="margin-top: 15px; font-size: 14px;">
            <li>가맹점명으로 검색</li>
            <li>지역별 가맹점 조회</li>
            <li>분야별 통계 및 필터링</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 사용 방법
st.markdown("---")
st.markdown("""
### 📖 사용 방법

1. **왼쪽 사이드바**를 확인하세요
2. 원하는 서비스를 클릭하세요
   - 🍴 **맛집검색**: 용인시 식당 정보 검색
   - 💳 **와이페이**: 와이페이 가맹점 조회
3. 각 페이지에서 제공하는 기능을 이용하세요
""")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>용인시 통합 정보 서비스 | Made with Streamlit</p>
    <p style="font-size: 0.9em;">데이터는 참고용이며 실제와 다를 수 있습니다</p>
</div>
""", unsafe_allow_html=True)
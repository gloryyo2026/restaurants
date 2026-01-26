import streamlit as st
import json
from urllib.parse import quote

# 1. 페이지 설정
st.set_page_config(
    page_title="용인시 맛집 검색",
    page_icon="🍴",
    layout="wide"
)

# 2. JSON 데이터 로드
@st.cache_data
def load_restaurant_data():
    try:
        with open('restaurants.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("restaurants.json 파일을 찾을 수 없습니다.")
        return {}

data = load_restaurant_data()

# 3. 타이틀
st.title("🍴 용인시 맛집 검색")
st.markdown("---")

# 4. 세션 상태 초기화
if 'selected_restaurant' not in st.session_state:
    st.session_state.selected_restaurant = None

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📍 지역 및 카테고리 선택")
    
    regions = list(data.keys())
    selected_region = st.selectbox("지역을 선택하세요", options=["선택하세요", "전체"] + regions)
    
    if selected_region != "선택하세요":
        if selected_region == "전체":
            all_cats = set()
            for r in data.values(): all_cats.update(r.keys())
            categories = sorted(list(all_cats))
        else:
            categories = list(data[selected_region].keys())
        
        selected_category = st.selectbox("메뉴 카테고리를 선택하세요", options=["선택하세요", "전체"] + categories)
        
        if selected_category != "선택하세요":
            st.markdown("### 🏪 식당 목록")
            restaurants = []
            for r_name, r_data in data.items():
                if selected_region in ["전체", r_name]:
                    for c_name, c_list in r_data.items():
                        if selected_category in ["전체", c_name]:
                            for res in c_list:
                                res_copy = res.copy()
                                res_copy['지역'] = r_name
                                res_copy['카테고리'] = c_name
                                restaurants.append(res_copy)
            
            st.info(f"총 {len(restaurants)}개의 식당 검색됨")
            for idx, res in enumerate(restaurants):
                if st.button(f"{res['식당명']} ({res['지역'].split()[-1]})", key=f"btn_{idx}", use_container_width=True):
                    st.session_state.selected_restaurant = res

with col2:
    st.subheader("🍽️ 식당 상세 정보")
    
    if st.session_state.selected_restaurant:
        res = st.session_state.selected_restaurant
        
        # HTML 코드를 변수에 먼저 담아 가독성과 오류를 방지합니다.
        # f-string 내부에서 CSS 중괄호를 쓰면 오류가 나므로 스타일을 최소화하거나 분리합니다.
        html_content = f"""
        <div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #eee; border-left: 8px solid #ff4b4b; color: #333;">
            <h2 style="color: #ff4b4b; margin: 0;">🏪 {res['식당명']}</h2>
            <p style="color: #888; margin-bottom: 20px;">📍 {res.get('지역','')} | 🍽️ {res.get('카테고리','')}</p>
            <hr>
            <h4 style="margin-bottom: 5px; color: #000;">💰 대표 메뉴 및 가격</h4>
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; color: #444;">
                {res['가격대'].replace(' / ', '<br>• ')}
            </div>
            <h4 style="margin: 20px 0 5px 0; color: #000;">📍 주소</h4>
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; color: #444;">
                {res['주소']}
            </div>
        </div>
        """
        # unsafe_allow_html=True가 핵심입니다.
        st.markdown(html_content, unsafe_allow_html=True)
        
        # 지도 버튼 섹션
        st.write("") 
        m1, m2, m3 = st.columns(3)
        q = quote(f"{res['식당명']} {res['주소']}")
        with m1: st.link_button("네이버 지도", f"https://map.naver.com/v5/search/{quote(res['식당명'])}", use_container_width=True)
        with m2: st.link_button("카카오맵", f"https://map.kakao.com/link/search/{q}", use_container_width=True)
        with m3: st.link_button("구글 지도", f"https://www.google.com/maps/search/{q}", use_container_width=True)
        
        if st.button("🔄 검색 초기화", use_container_width=True):
            st.session_state.selected_restaurant = None
            st.rerun()
    else:
        st.info("왼쪽 리스트에서 식당을 선택해 주세요.")

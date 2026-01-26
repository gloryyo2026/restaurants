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
                # 지역명을 포함하여 버튼 표시
                btn_label = f"{res['식당명']} ({res['지역'].split()[-1]})"
                if st.button(btn_label, key=f"btn_{idx}", use_container_width=True):
                    st.session_state.selected_restaurant = res

with col2:
    st.subheader("🍽️ 식당 상세 정보")
    
    if st.session_state.selected_restaurant:
        res = st.session_state.selected_restaurant
        
        # [수정 핵심] 가격 정보의 첫 번째 항목에도 불렛을 붙이고 정렬합니다.
        raw_price = res['가격대']
        formatted_price = "• " + raw_price.replace(' / ', '<br>• ')
        
        # 가독성을 높인 HTML 카드 구조
        html_content = f"""
        <div style="background-color: white; padding: 25px; border-radius: 12px; border: 1px solid #eee; border-left: 10px solid #ff4b4b; color: #333; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <h2 style="color: #ff4b4b; margin: 0 0 5px 0; font-size: 26px;">🏪 {res['식당명']}</h2>
            <p style="color: #777; font-size: 14px; margin-bottom: 25px;">📍 {res.get('지역','')} | 🍽️ {res.get('카테고리','')}</p>
            
            <div style="margin-bottom: 20px;">
                <h4 style="margin-bottom: 10px; color: #111; font-size: 18px;">💰 대표 메뉴 및 가격</h4>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; color: #444; line-height: 1.8; font-size: 16px;">
                    {formatted_price}
                </div>
            </div>
            
            <div>
                <h4 style="margin-bottom: 10px; color: #111; font-size: 18px;">📍 주소</h4>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; color: #444; font-size: 15px;">
                    {res['주소']}
                </div>
            </div>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
        
        # 지도 버튼 섹션
        st.write("") 
        m1, m2, m3 = st.columns(3)
        # 검색어 최적화
        search_term = f"{res['식당명']} {res['주소']}"
        q = quote(search_term)
        
        with m1: st.link_button("네이버 지도", f"https://map.naver.com/v5/search/{quote(res['식당명'])}", use_container_width=True)
        with m2: st.link_button("카카오맵", f"https://map.kakao.com/link/search/{q}", use_container_width=True)
        with m3: st.link_button("구글 지도", f"https://www.google.com/maps/search/{q}", use_container_width=True)
        
        if st.button("🔄 검색 초기화", use_container_width=True):
            st.session_state.selected_restaurant = None
            st.rerun()
    else:
        st.info("👈 왼쪽 리스트에서 식당을 선택해 주세요.")

# 푸터
st.markdown("---")
st.markdown('<p style="text-align: center; color: #999; font-size: 12px;">© 2026 용인시 맛집 가이드</p>', unsafe_allow_html=True)

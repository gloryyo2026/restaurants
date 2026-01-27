import streamlit as st
import json
from urllib.parse import quote

# 1. 페이지 설정
st.set_page_config(
    page_title="용인지역 가본 맛집 검색",
    page_icon="🍴",
    layout="wide"
)

# 2. JSON 데이터 로드
@st.cache_data
def load_restaurant_data():
    try:
        # 새로 수정하신 영업시간이 포함된 json 파일명을 확인해주세요.
        with open('restaurants.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("restaurants.json 파일을 찾을 수 없습니다. 파일명이 정확한지 확인해주세요.")
        return {}

data = load_restaurant_data()

# 3. 타이틀
st.title("🍴 용인시 맛집 검색")
st.markdown("---")

# 4. 세션 상태 초기화
if 'selected_restaurant' not in st.session_state:
    st.session_state.selected_restaurant = None

# 5. 레이아웃: 컬럼 설정
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
                loc_short = res['지역'].split()[-1]
                if st.button(f"{res['식당명']} ({loc_short})", key=f"btn_{idx}", use_container_width=True):
                    st.session_state.selected_restaurant = res

with col2:
    st.subheader("🍽️ 식당 상세 정보")
    
    if st.session_state.selected_restaurant:
        res = st.session_state.selected_restaurant
        
        # 💰 가격 정보 포맷팅 (모든 항목에 불릿 추가)
        raw_price = res.get('가격대', '정보 없음')
        formatted_price = "• " + raw_price.replace(' / ', '<br>• ')
        
        # ⏰ 영업시간 정보 가져오기 (데이터에 없을 경우를 대비해 기본값 설정)
        opening_hours = res.get('영업시간', '영업시간 정보가 등록되지 않았습니다.')
        
        # ⚠️ HTML 노출 방지를 위해 들여쓰기 공백 없이 한 줄로 결합
        html_card = (
            f'<div style="background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #ddd; border-left: 10px solid #ff4b4b; color: #222222; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">'
            f'<h2 style="color: #ff4b4b; margin: 0 0 5px 0; font-size: 24px;">🏪 {res["식당명"]}</h2>'
            f'<p style="color: #666666; font-size: 14px; margin-bottom: 20px;">📍 {res.get("지역","")} | 🍽️ {res.get("카테고리","")}</p>'
            f'<hr style="border: 0.5px solid #eee; margin: 15px 0;">'
            f'<h4 style="margin: 0 0 10px 0; color: #111111; font-size: 18px;">⏰ 영업시간</h4>'
            f'<div style="background-color: #fff9f9; padding: 15px; border-radius: 8px; color: #d32f2f; font-weight: 500; margin-bottom: 20px; border: 1px dashed #ffcdd2;">{opening_hours}</div>'
            f'<h4 style="margin: 0 0 10px 0; color: #111111; font-size: 18px;">💰 대표 메뉴 및 가격</h4>'
            f'<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; color: #333333; line-height: 1.7; font-size: 16px; margin-bottom: 20px;">{formatted_price}</div>'
            f'<h4 style="margin: 0 0 10px 0; color: #111111; font-size: 18px;">📍 주소</h4>'
            f'<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; color: #333333; font-size: 15px;">{res["주소"]}</div>'
            f'</div>'
        )
        
        # HTML 렌더링
        st.markdown(html_card, unsafe_allow_html=True)
        
        # 🗺️ 지도 및 기타 액션
        st.write("") 
        m1, m2, m3 = st.columns(3)
        q_full = quote(f"{res['식당명']} {res['주소']}")
        
        with m1: st.link_button("네이버 지도", f"https://map.naver.com/v5/search/{quote(res['식당명'])}", use_container_width=True)
        with m2: st.link_button("카카오맵", f"https://map.kakao.com/link/search/{q_full}", use_container_width=True)
        with m3: st.link_button("구글 지도", f"https://www.google.com/maps/search/{q_full}", use_container_width=True)
        
        if st.button("🔄 다시 검색하기", use_container_width=True):
            st.session_state.selected_restaurant = None
            st.rerun()
    else:
        st.info("👈 위에서 지역과 음식 종류를 고른 후 식당을 선택하면 상세 정보가 이곳에 표시됩니다.")

# 푸터
st.markdown("---")
st.markdown('<p style="text-align: center; color: #999; font-size: 12px;">용인시 맛집 검색 서비스 | 데이터는 실제 정보와 다를 수 있습니다.</p>', unsafe_allow_html=True)


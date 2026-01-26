import streamlit as st
import json
from urllib.parse import quote

# 1. 페이지 설정
st.set_page_config(
    page_title="용인시 맛집 검색",
    page_icon="🍴",
    layout="wide"
)

# 2. JSON 데이터 로드 함수
@st.cache_data
def load_restaurant_data():
    try:
        # 파일명을 본인의 환경에 맞게 확인하세요 (예: 'restaurants.json')
        with open('restaurants.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("restaurants.json 파일을 찾을 수 없습니다. 파일을 같은 폴더에 넣어주세요.")
        return {}

# 데이터 로드
data = load_restaurant_data()

# 3. 타이틀 및 스타일 설정
st.title("🍴 용인시 맛집 검색")
st.markdown("""
    <style>
    /* 모바일에서 버튼 텍스트가 잘리지 않도록 설정 */
    .stButton>button {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown("---")

# 4. 세션 상태 초기화
if 'selected_restaurant' not in st.session_state:
    st.session_state.selected_restaurant = None

# 5. 레이아웃: 2개의 컬럼 (모바일에서는 자동으로 위아래 배치됨)
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📍 지역 및 카테고리 선택")
    
    # 지역 선택
    regions = list(data.keys())
    selected_region = st.selectbox(
        "지역을 선택하세요",
        options=["선택하세요", "전체"] + regions,
        key="region"
    )
    
    # 카테고리 선택 (지역이 선택된 경우에만)
    if selected_region != "선택하세요":
        if selected_region == "전체":
            all_categories = set()
            for r_data in data.values():
                all_categories.update(r_data.keys())
            categories = sorted(list(all_categories))
        else:
            categories = list(data[selected_region].keys())
        
        selected_category = st.selectbox(
            "메뉴 카테고리를 선택하세요",
            options=["선택하세요", "전체"] + categories,
            key="category"
        )
        
        # 식당 리스트 로직
        if selected_category != "선택하세요":
            st.markdown("---")
            st.markdown("### 🏪 식당 목록")
            
            restaurants = []
            
            # 데이터 필터링
            for r_name, r_data in data.items():
                if selected_region == "전체" or selected_region == r_name:
                    for c_name, c_list in r_data.items():
                        if selected_category == "전체" or selected_category == c_name:
                            for res in c_list:
                                temp_res = res.copy()
                                temp_res['지역'] = r_name
                                temp_res['카테고리'] = c_name
                                restaurants.append(temp_res)
            
            st.info(f"총 {len(restaurants)}개의 식당이 검색되었습니다.")
            
            # 식당 선택 버튼 생성
            for idx, restaurant in enumerate(restaurants):
                display_text = f"{restaurant['식당명']}"
                if selected_region == "전체":
                    display_text += f" [{restaurant['지역'].replace('용인시 ', '')}]"
                
                if st.button(display_text, key=f"res_{idx}", use_container_width=True):
                    st.session_state.selected_restaurant = restaurant

with col2:
    st.subheader("🍽️ 식당 상세 정보")
    
    if st.session_state.selected_restaurant:
        res = st.session_state.selected_restaurant
        
        # 가독성 해결을 위한 명시적 스타일 (배경 흰색, 글자 진한 회색 고정)
        st.markdown(f"""
        <div style="
            background-color: #ffffff;
            padding: 25px;
            border-radius: 15px;
            border: 1px solid #ddd;
            border-left: 10px solid #ff4b4b;
            color: #222222;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        ">
            <h2 style="color: #ff4b4b; margin: 0 0 10px 0; font-size: 24px;">🏪 {res['식당명']}</h2>
            <p style="color: #777; font-size: 14px; margin-bottom: 20px;">
                📍 {res['지역']} | 🍽️ {res['카테고리']}
            </p>
            
            <div style="margin-bottom: 20px;">
                <h4 style="color: #333; margin-bottom: 8px;">💰 대표 메뉴 및 가격</h4>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; font-size: 16px; line-height: 1.6; color: #333;">
                    {res['가격대'].replace(' / ', '<br>• ')}
                </div>
            </div>
            
            <div>
                <h4 style="color: #333; margin-bottom: 8px;">📍 주소</h4>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; font-size: 15px; color: #555;">
                    {res['주소']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 지도 연결 버튼
        st.markdown("### 🗺️ 지도 앱으로 보기")
        m_col1, m_col2, m_col3 = st.columns(3)
        
        query_simple = quote(f"{res['식당명']} 용인")
        query_full = quote(f"{res['식당명']} {res['주소']}")

        with m_col1:
            st.link_button("네이버 지도", f"https://map.naver.com/v5/search/{query_simple}", use_container_width=True)
        with m_col2:
            st.link_button("카카오맵", f"https://map.kakao.com/link/search/{query_full}", use_container_width=True)
        with m_col3:
            st.link_button("구글 지도", f"https://www.google.com/maps/search/{query_full}", use_container_width=True)
            
        if st.button("🔄 검색 초기화", use_container_width=True):
            st.session_state.selected_restaurant = None
            st.rerun()
            
    else:
        st.info("👈 왼쪽에서 식당을 선택하면 상세 정보가 표시됩니다.")
        st.image("https://via.placeholder.com/800x400/f0f2f6/666666?text=Select+a+Restaurant", use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">
        © 2026 용인시 맛집 가이드 | 제공된 정보는 실제와 다를 수 있습니다.
    </div>
    """, unsafe_allow_html=True)

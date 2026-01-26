import streamlit as st
import json

# 페이지 설정
st.set_page_config(
    page_title="용인시 맛집 검색",
    page_icon="🍴",
    layout="wide"
)

# JSON 파일 로드
@st.cache_data
def load_restaurant_data():
    try:
        with open('restaurants.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("restaurants.json 파일을 찾을 수 없습니다. 파일을 같은 폴더에 넣어주세요.")
        return {}

# 데이터 로드
data = load_restaurant_data()

# 타이틀
st.title("🍴 용인시 맛집 검색")
st.markdown("---")

# 세션 상태 초기화
if 'selected_restaurant' not in st.session_state:
    st.session_state.selected_restaurant = None

# 레이아웃: 2개의 컬럼
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📍 지역 및 카테고리 선택")
    
    # 1. 지역 선택
    regions = list(data.keys())
    selected_region = st.selectbox(
        "지역을 선택하세요",
        options=["선택하세요", "전체"] + regions,
        key="region"
    )
    
    # 2. 카테고리 선택 (지역이 선택된 경우에만)
    if selected_region != "선택하세요":
        # 전체 지역이 선택된 경우 모든 카테고리 수집
        if selected_region == "전체":
            all_categories = set()
            for region in data.values():
                all_categories.update(region.keys())
            categories = sorted(list(all_categories))
        else:
            categories = list(data[selected_region].keys())
        
        selected_category = st.selectbox(
            "메뉴 카테고리를 선택하세요",
            options=["선택하세요", "전체"] + categories,
            key="category"
        )
        
        # 3. 식당 리스트 표시 (카테고리가 선택된 경우에만)
        if selected_category != "선택하세요":
            st.markdown("### 🏪 식당 목록")
            
            # 식당 리스트 수집
            restaurants = []
            
            if selected_region == "전체" and selected_category == "전체":
                # 모든 지역, 모든 카테고리
                for region_name, region_data in data.items():
                    for category_name, category_restaurants in region_data.items():
                        for restaurant in category_restaurants:
                            restaurant_with_info = restaurant.copy()
                            restaurant_with_info['지역'] = region_name
                            restaurant_with_info['카테고리'] = category_name
                            restaurants.append(restaurant_with_info)
            
            elif selected_region == "전체":
                # 모든 지역, 특정 카테고리
                for region_name, region_data in data.items():
                    if selected_category in region_data:
                        for restaurant in region_data[selected_category]:
                            restaurant_with_info = restaurant.copy()
                            restaurant_with_info['지역'] = region_name
                            restaurant_with_info['카테고리'] = selected_category
                            restaurants.append(restaurant_with_info)
            
            elif selected_category == "전체":
                # 특정 지역, 모든 카테고리
                for category_name, category_restaurants in data[selected_region].items():
                    for restaurant in category_restaurants:
                        restaurant_with_info = restaurant.copy()
                        restaurant_with_info['지역'] = selected_region
                        restaurant_with_info['카테고리'] = category_name
                        restaurants.append(restaurant_with_info)
            
            else:
                # 특정 지역, 특정 카테고리
                for restaurant in data[selected_region][selected_category]:
                    restaurant_with_info = restaurant.copy()
                    restaurant_with_info['지역'] = selected_region
                    restaurant_with_info['카테고리'] = selected_category
                    restaurants.append(restaurant_with_info)
            
            # 식당 개수 표시
            st.info(f"총 {len(restaurants)}개의 식당이 검색되었습니다.")
            
            # 식당 버튼 리스트
            for idx, restaurant in enumerate(restaurants):
                # 지역/카테고리 정보 표시 (전체 선택 시)
                display_text = f"{restaurant['식당명']}"
                if '지역' in restaurant:
                    display_text += f" [{restaurant['지역'].replace('용인시 ', '')}]"
                if '카테고리' in restaurant and (selected_category == "전체" or selected_region == "전체"):
                    display_text += f" - {restaurant['카테고리']}"
                
                if st.button(
                    display_text,
                    key=f"restaurant_{idx}",
                    use_container_width=True
                ):
                    st.session_state.selected_restaurant = restaurant

with col2:
    st.subheader("🍽️ 식당 상세 정보")
    
    if st.session_state.selected_restaurant:
        restaurant = st.session_state.selected_restaurant
        
        # 식당 정보 카드 스타일로 표시
        region_info = f"<p style='color: #888; font-size: 14px;'>📍 {restaurant.get('지역', '')} | 🍽️ {restaurant.get('카테고리', '')}</p>" if '지역' in restaurant else ""
        
        st.markdown(f"""
        <div style="
            background-color: #f0f2f6;
            padding: 30px;
            border-radius: 10px;
            border-left: 5px solid #ff4b4b;
        ">
            <h2 style="color: #ff4b4b; margin-top: 0;">🏪 {restaurant['식당명']}</h2>
            {region_info}
            <hr style="margin: 20px 0;">
            <h3>💰 가격 정보</h3>
            <p style="font-size: 18px; line-height: 1.8;">
                {restaurant['가격대'].replace(' / ', '<br>• ')}
            </p>
            <hr style="margin: 20px 0;">
            <h3>📍 주소</h3>
            <p style="font-size: 16px; color: #555;">
                {restaurant['주소']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 지도 링크 버튼들
        st.markdown("### 🗺️ 지도에서 보기")
        map_col1, map_col2, map_col3 = st.columns(3)
        
        # URL 인코딩을 위한 import
        from urllib.parse import quote
        
        # 검색어 최적화: 식당명 + 간단한 지역명
        address_parts = restaurant['주소'].split()
        simple_location = ' '.join(address_parts[:3])  # 예: 경기도 용인시 기흥구
        
        with map_col1:
            # 네이버 지도: 식당명만으로 검색
            search_query = quote(f"{restaurant['식당명']} 용인")
            naver_map_url = f"https://map.naver.com/v5/search/{search_query}"
            st.link_button("🗺️ 네이버 지도", naver_map_url, use_container_width=True)
        
        with map_col2:
            # 카카오맵: 식당명 + 간단한 주소
            kakao_query = quote(f"{restaurant['식당명']} {simple_location}")
            kakao_map_url = f"https://map.kakao.com/link/search/{kakao_query}"
            st.link_button("🗺️ 카카오맵", kakao_map_url, use_container_width=True)
        
        with map_col3:
            # 구글 지도
            google_query = quote(f"{restaurant['식당명']} {restaurant['주소']}")
            google_map_url = f"https://www.google.com/maps/search/{google_query}"
            st.link_button("🗺️ 구글 지도", google_map_url, use_container_width=True)
        
        # 초기화 버튼
        if st.button("🔄 다시 검색하기", use_container_width=True):
            st.session_state.selected_restaurant = None
            st.rerun()
    else:
        st.info("👈 왼쪽에서 지역과 카테고리를 선택한 후, 식당을 클릭하면 상세 정보가 표시됩니다.")
        st.image("https://via.placeholder.com/600x400/f0f2f6/666666?text=식당을+선택해주세요", use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>용인시 맛집 정보 | 데이터는 참고용이며, 실제 가격과 다를 수 있습니다.</p>
</div>
""", unsafe_allow_html=True)
import streamlit as st
import requests
import random
from datetime import datetime

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="오하아사 X NASA 우주 운세",
    page_icon="🌌",
    layout="centered"
)

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .fortune-card {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- API 키 설정 ---
# 깃허브 올릴 때 직접 키를 적지 않고 Streamlit Secrets 기능을 활용합니다.
NASA_API_KEY = st.secrets.get("NASA_API_KEY", "DEMO_KEY")

# --- 데이터 준비 (오하아사 별자리 및 럭키 아이템 모의 데이터) ---
ZODIACS = ["양자리", "황소자리", "쌍둥이자리", "게자리", "사자자리", "처녀자리", 
           "천칭자리", "전갈자리", "사수자리", "염소자리", "물병자리", "물고기자리"]

LUCKY_ITEMS = ["초록색 우산", "빈티지 열쇠고리", "메탈 시계", "우주 스티커", "따뜻한 코코아", "파란색 펜"]
LUCKY_COLORS = ["네이비", "크림 옐로우", "네온 그린", "마젠타", "실버", "로즈 골드"]
ADVICES = [
    "오늘은 직관을 믿고 새로운 도전을 해보세요!",
    "주변 사람들과의 소통에서 뜻밖의 행운이 찾아옵니다.",
    "차분하게 주변을 정리하면 집중력이 올라갑니다.",
    "작은 실수가 생기더라도 긍정적인 마음가짐이 중요합니다."
]

# --- NASA API 호출 함수 (오늘의 우주 사진) ---
@st.cache_data(ttl=3600)
def get_nasa_apod():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"NASA API 연결 실패: {e}")
    return None

# --- UI 레이아웃 ---
st.title("🌌 오하아사 X NASA 우주 운세 탐구실")
st.write("오늘의 우주 기상 데이터와 별자리 운세를 융합하여 당신의 하루를 전달합니다.")

st.divider()

# 1. 별자리 선택
selected_zodiac = st.selectbox("🔮 당신의 별자리를 선택하세요:", ZODIACS)

# 날짜 기반 시드 설정 (매일 같은 별자리는 동일한 운세를 얻도록 처리)
today_str = datetime.now().strftime("%Y-%m-%d")
seed_value = hash(today_str + selected_zodiac)
random.seed(seed_value)

# 운세 데이터 생성
rank = random.randint(1, 12)
score = random.randint(60, 100)
item = random.choice(LUCKY_ITEMS)
color = random.choice(LUCKY_COLORS)
advice = random.choice(ADVICES)

# 2. 운세 결과 출력
st.subheader(f"✨ {selected_zodiac}의 오늘 운세")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="오하아사 순위", value=f"{rank} 위 / 12위")
with col2:
    st.metric(label="운세 지수", value=f"{score} 점")

st.markdown(f"""
<div class="fortune-card">
    <h4>🍀 오늘의 행운 요소</h4>
    <ul>
        <li><b>럭키 아이템:</b> {item}</li>
        <li><b>럭키 컬러:</b> {color}</li>
    </ul>
    <p><b>💡 오늘의 조언:</b> {advice}</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# 3. NASA 우주 데이터 연동 파트
st.subheader("🪐 오늘의 NASA 우주 데이터 (APOD)")
apod_data = get_nasa_apod()

if apod_data:
    st.write(f"**제목:** {apod_data.get('title', 'NASA Picture of the Day')}")
    
    # 미디어 타입에 따른 출력 (이미지 또는 비디오)
    media_type = apod_data.get("media_type")
    if media_type == "image":
        st.image(apod_data.get("url"), caption=f"Photo by NASA ({apod_data.get('date')})", use_column_width=True)
    elif media_type == "video":
        st.video(apod_data.get("url"))
        
    with st.expander("📖 NASA의 오늘 우주 설명 보기 (원문)"):
        st.write(apod_data.get("explanation", "설명이 제공되지 않았습니다."))
else:
    st.info("현재 NASA 우주 데이터를 불러오는 중이거나 DEMO 키 한도에 도달했습니다.")

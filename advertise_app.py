import streamlit as st
import pandas as pd
import joblib

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="광고 매출 예측 AI",
    page_icon="📊",
    layout="wide"
)

# =========================
# 모델 불러오기
# =========================
model = joblib.load("advertise_model.pkl")

# =========================
# CSS 스타일
# =========================
st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
}

h1 {
    color: #1e3a8a;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg,#2563eb,#1d4ed8);
    color: white;
    border: none;
    border-radius: 12px;
    height: 3.2rem;
    font-size: 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #1d4ed8;
    color: white;
}

[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# =========================
# 사이드바
# =========================
with st.sidebar:
    st.title("📋 프로젝트 정보")

    st.markdown("""
    **광고 매출 예측 시스템**

    머신러닝 모델을 활용하여

    - TV 광고비
    - 라디오 광고비
    - 신문 광고비

    를 기반으로 예상 매출을 예측합니다.
    """)

    st.divider()

    st.info("모델: Linear Regression")

# =========================
# 메인 제목
# =========================
st.title("📊 광고 매출 예측 AI")

st.markdown("""
광고 예산을 입력하면 AI가 예상 매출을 분석합니다.
""")

st.info("💡 화폐 단위: 천 달러($1,000) 기준")

st.divider()

# =========================
# 입력 영역
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    tv_input = st.number_input(
        "📺 TV 광고비",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

with col2:
    radio_input = st.number_input(
        "📻 라디오 광고비",
        min_value=0.0,
        value=20.0,
        step=1.0
    )

with col3:
    newspaper_input = st.number_input(
        "📰 신문 광고비",
        min_value=0.0,
        value=10.0,
        step=1.0
    )

st.write("")

# =========================
# 예측 버튼
# =========================
if st.button("🚀 AI 분석 실행"):

    try:
        feature_names = list(model.feature_names_in_)

        new_store_data = pd.DataFrame(
            [[tv_input, radio_input, newspaper_input]],
            columns=feature_names
        )

        predicted_sales = model.predict(new_store_data)

        st.divider()

        st.subheader("📈 분석 결과")

        # KPI 카드
        colA, colB = st.columns(2)

        with colA:
            st.metric(
                "예상 매출",
                f"${predicted_sales[0] * 1000:,.0f}"
            )

        with colB:
            total_budget = tv_input + radio_input + newspaper_input

            st.metric(
                "총 광고비",
                f"${total_budget * 1000:,.0f}"
            )

        st.success(
            f"AI 예측 결과 예상 매출은 약 {predicted_sales[0]:.2f}천 달러입니다."
        )

        # 광고비 그래프
        st.subheader("📊 광고비 분포")

        chart_data = pd.DataFrame({
            "광고비": [
                tv_input,
                radio_input,
                newspaper_input
            ]
        },
        index=["TV", "Radio", "Newspaper"])

        st.bar_chart(chart_data)

    except Exception as e:
        st.error(f"오류 발생: {e}")

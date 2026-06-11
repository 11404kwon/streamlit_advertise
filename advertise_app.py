import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# =====================================
# 페이지 설정
# =====================================
st.set_page_config(
    page_title="Marketing Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================
# 모델 로드
# =====================================
model = joblib.load("advertise_model.pkl")

# =====================================
# CSS
# =====================================
st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 1.5rem;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
}

[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:15px;
    border:1px solid #e5e7eb;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}

.stButton > button {
    width:100%;
    height:3.2rem;
    border-radius:12px;
    font-weight:bold;
    font-size:17px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# 사이드바
# =====================================
with st.sidebar:

    st.title("📋 Dashboard Info")

    st.markdown("""
### 광고 성과 예측 시스템

AI 모델을 이용하여

- TV 광고
- Radio 광고
- Newspaper 광고

예산을 기반으로
예상 판매량을 예측합니다.
""")

    st.divider()

    st.success("Model Loaded")

# =====================================
# 헤더
# =====================================
st.title("📊 Marketing Performance Dashboard")

st.caption(
    "AI-Powered Advertising Forecast System"
)

st.divider()

# =====================================
# 탭
# =====================================
tab1, tab2, tab3 = st.tabs([
    "📈 예측",
    "📊 광고 분석",
    "ℹ️ 모델 정보"
])

# =====================================
# TAB1
# =====================================
with tab1:

    st.subheader("광고 예산 입력")

    col1, col2, col3 = st.columns(3)

    with col1:
        tv_input = st.number_input(
            "📺 TV",
            min_value=0.0,
            value=100.0,
            step=1.0
        )

    with col2:
        radio_input = st.number_input(
            "📻 Radio",
            min_value=0.0,
            value=20.0,
            step=1.0
        )

    with col3:
        newspaper_input = st.number_input(
            "📰 Newspaper",
            min_value=0.0,
            value=10.0,
            step=1.0
        )

    st.write("")

    if st.button("🚀 AI 분석 실행"):

        feature_names = list(model.feature_names_in_)

        new_data = pd.DataFrame(
            [[tv_input, radio_input, newspaper_input]],
            columns=feature_names
        )

        prediction = model.predict(new_data)[0]

        total_budget = (
            tv_input +
            radio_input +
            newspaper_input
        )

        roi = prediction / total_budget

        st.divider()

        # KPI 카드
        k1, k2, k3 = st.columns(3)

        with k1:
            st.metric(
                "예상 판매량",
                f"{prediction:.2f}"
            )

        with k2:
            st.metric(
                "총 광고비",
                f"${total_budget:,.0f}K"
            )

        with k3:
            st.metric(
                "광고 효율 지수",
                f"{roi:.3f}"
            )

        st.success(
            f"AI는 약 {prediction:.2f}의 판매 성과를 예측했습니다."
        )

        # 인사이트
        st.subheader("🤖 AI Insight")

        dominant = max(
            tv_input,
            radio_input,
            newspaper_input
        )

        if dominant == tv_input:
            st.info(
                "TV 광고가 전체 예산의 가장 큰 비중을 차지합니다."
            )

        elif dominant == radio_input:
            st.info(
                "Radio 광고 의존도가 높은 전략입니다."
            )

        else:
            st.info(
                "Newspaper 광고 비중이 높은 전략입니다."
            )

# =====================================
# TAB2
# =====================================
with tab2:

    st.subheader("광고비 분석")

    budget_df = pd.DataFrame({
        "매체": [
            "TV",
            "Radio",
            "Newspaper"
        ],
        "광고비": [
            tv_input,
            radio_input,
            newspaper_input
        ]
    })

    c1, c2 = st.columns(2)

    with c1:

        fig1 = px.pie(
            budget_df,
            values="광고비",
            names="매체",
            hole=0.55,
            title="광고비 비중"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with c2:

        fig2 = px.bar(
            budget_df,
            x="매체",
            y="광고비",
            title="매체별 광고비"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# =====================================
# TAB3
# =====================================
with tab3:

    st.subheader("모델 정보")

    st.markdown("""
### 사용 모델

- Linear Regression

### 입력 변수

- TV 광고비
- Radio 광고비
- Newspaper 광고비

### 출력 변수

- 예상 판매량

### 목적

광고 예산에 따른 판매 성과를
예측하여 마케팅 의사결정을 지원합니다.
""")

import streamlit as st
import pandas as pd
import joblib

# =========================
# 모델 불러오기
# =========================
model = joblib.load("advertise_model.pkl")

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="광고 매출 예측 AI",
    page_icon="📈",
    layout="centered"
)

# =========================
# 제목
# =========================
st.title("📈 광고 매출 예측 AI")
st.markdown("광고비를 입력하면 AI가 예상 매출을 예측합니다.")

st.info(
    "💡 화폐 단위: 천 달러($1,000) 기준\n\n"
    "예: 100 입력 → $100,000"
)

st.divider()

# =========================
# 광고비 입력
# =========================
tv_input = st.number_input(
    "📺 TV 광고비 (천 달러)",
    min_value=0.0,
    value=100.0,
    step=1.0
)

radio_input = st.number_input(
    "📻 라디오 광고비 (천 달러)",
    min_value=0.0,
    value=20.0,
    step=1.0
)

newspaper_input = st.number_input(
    "📰 신문 광고비 (천 달러)",
    min_value=0.0,
    value=10.0,
    step=1.0
)

# =========================
# 예측
# =========================
if st.button("🚀 매출 예측하기", use_container_width=True):

    new_store_data = pd.DataFrame(
        [[tv_input, radio_input, newspaper_input]],
        columns=["TV", "Radio", "Newspaper"]
    )

    predicted_sales = model.predict(new_store_data)

    st.divider()

    st.subheader("🎯 AI 예측 결과")

    st.success(
        f"예상 매출은 약 {predicted_sales[0]:.2f}천 달러입니다."
    )

    st.metric(
        label="예상 매출",
        value=f"${predicted_sales[0] * 1000:,.0f}"
    )

    st.caption(
        "※ 예측값은 머신러닝 모델을 기반으로 계산된 추정치입니다."
    )

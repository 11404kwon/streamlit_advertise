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
st.write("광고비를 입력하면 AI가 예상 매출을 예측합니다.")

st.info("💡 화폐 단위: 천 달러($1,000) 기준")

# =========================
# 입력
# =========================
tv_input = st.number_input(
    "📺 TV 광고비",
    min_value=0.0,
    value=100.0
)

radio_input = st.number_input(
    "📻 라디오 광고비",
    min_value=0.0,
    value=20.0
)

newspaper_input = st.number_input(
    "📰 신문 광고비",
    min_value=0.0,
    value=10.0
)

# =========================
# 예측
# =========================
if st.button("🚀 매출 예측하기"):

    try:
        # 모델이 학습한 컬럼명 자동 가져오기
        feature_names = list(model.feature_names_in_)

        # 입력값 매핑
        values = [tv_input, radio_input, newspaper_input]

        new_store_data = pd.DataFrame(
            [values],
            columns=feature_names
        )

        predicted_sales = model.predict(new_store_data)

        st.success(
            f"예상 매출: {predicted_sales[0]:.2f}천 달러"
        )

        st.metric(
            "예상 매출",
            f"${predicted_sales[0] * 1000:,.0f}"
        )

    except Exception as e:
        st.error(f"오류 발생: {e}")

        st.subheader("모델 정보")

        try:
            st.write("학습 컬럼명:")
            st.write(model.feature_names_in_)
        except:
            st.write("feature_names_in_ 정보를 찾을 수 없습니다.")

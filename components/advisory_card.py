import streamlit as st
from models.explainer import explain_aqi
from datetime import datetime

def render_advisory(city_name, row):
    month = datetime.now().month
    reasons, recommendations = explain_aqi(row, month)

    st.markdown(f"### 🔍 Why is AQI high in {city_name} today?")

    with st.expander("See explanation", expanded=True):
        for r in reasons:
            st.markdown(f"- {r}")

    st.markdown("### 💊 What should you do?")
    for rec in recommendations:
        st.markdown(f"✅ {rec}")

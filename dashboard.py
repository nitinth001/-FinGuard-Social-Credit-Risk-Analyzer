import streamlit as st
import requests
import pandas as pd

# Set page config
st.set_page_config(page_title="FinGuard AI", page_icon="🛡️")

st.title("🛡️ FinGuard: Social Credit Risk Analyzer")
st.markdown("---")

# Sidebar for inputs
st.sidebar.header("User Profile Features")

name = st.sidebar.text_input("Candidate Name", "John Doe")
tenure = st.sidebar.slider("Avg Job Tenure (Months)", 0, 72, 24)
total_exp = st.sidebar.slider("Total Experience (Months)", 0, 240, 60)
hops = st.sidebar.number_input("Job Hops (Last 2 Years)", 0, 10, 1)
network = st.sidebar.slider("Professional Network Score", 0, 100, 50)
sentiment = st.sidebar.slider("Headline Sentiment (-1 to 1)", -1.0, 1.0, 0.2)
consistency = st.sidebar.slider("Activity Consistency", 0.0, 1.0, 0.5)

# When user clicks the button
if st.button("Generate Risk Analysis Report"):
    # The JSON data to send to your FastAPI
    payload = {
        "name": name,
        "avg_tenure_months": tenure,
        "total_exp_months": total_exp,
        "recent_hops": hops,
        "network_score": network,
        "sentiment": sentiment,
        "consistency_index": consistency
    }

    try:
        # Connect to your FastAPI endpoint
        response = requests.post("http://127.0.0.1:8000/analyze", json=payload)
        res_data = response.json()

        # Display results in columns
        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="Reliability Score", value=res_data["reliability_score"])
            
            color = "green" if res_data["risk_category"] == "GREEN" else "red"
            st.markdown(f"Risk Status: **:{color}[{res_data['risk_category']}]**")

        with col2:
            st.subheader("AI Narrative")
            st.write(res_data["ai_narrative"])

        st.info(f"**Flags:** {res_data['behavioral_flags']}")

    except Exception as e:
        st.error(f"Could not connect to the Backend API. Make sure app.py is running! Error: {e}")
import streamlit as st
import requests

# ---------------- CONFIG ----------------
BASE_URL = "http://127.0.0.1:8000"  # FastAPI URL

# ---------------- SESSION STATE ----------------
if "token" not in st.session_state:
    st.session_state.token = None

st.set_page_config(page_title="JWT Auth Prediction App", layout="centered")
st.title("🔐 JWT Authentication + Prediction")

# ---------------- AUTH SECTION ----------------
st.subheader("Register / Login")

tab1, tab2 = st.tabs(["Register", "Login"])

with tab1:
    reg_username = st.text_input("Username", key="reg_user")
    reg_password = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Register"):
        payload = {
            "username": reg_username,
            "password": reg_password
        }
        res = requests.post(f"{BASE_URL}/register", json=payload)

        if res.status_code == 200:
            data = res.json()
            st.session_state.token = data["access_token"]
            st.success("Registered successfully 🎉")
        else:
            st.error(res.json()["detail"])

with tab2:
    login_username = st.text_input("Username", key="login_user")
    login_password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        payload = {
            "username": login_username,
            "password": login_password
        }
        res = requests.post(f"{BASE_URL}/login", json=payload)

        if res.status_code == 200:
            data = res.json()
            st.session_state.token = data["access_token"]
            st.success("Logged in successfully ✅")
        else:
            st.error(res.json()["detail"])

# ---------------- PREDICTION SECTION ----------------
st.divider()
st.subheader("🔮 Prediction (Protected Route)")

if st.session_state.token is None:
    st.warning("Please login first to access prediction.")
else:
    st.success("Authenticated ✔️")

    # -------- CUSTOMER DATA (MATCH YOUR CustomerData MODEL) --------
    age = st.number_input("Age", min_value=1, max_value=100)
    income = st.number_input("Income", min_value=0)
    loan_amount = st.number_input("Loan Amount", min_value=0)
    credit_score = st.number_input("Credit Score", min_value=300, max_value=900)

    if st.button("Predict"):
        payload = {
            "customer": {
                "age": age,
                "income": income,
                "loan_amount": loan_amount,
                "credit_score": credit_score
            }
        }

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        res = requests.post(
            f"{BASE_URL}/predict/auth",
            json=payload,
            headers=headers
        )

        if res.status_code == 200:
            st.success("Prediction Successful 🎯")
            st.json(res.json())
        else:
            st.error(res.json())

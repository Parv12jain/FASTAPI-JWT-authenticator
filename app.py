# import streamlit as st
# import requests

# # ---------------- CONFIG ----------------
# BASE_URL = "http://127.0.0.1:8000"  # FastAPI URL

# # ---------------- SESSION STATE ----------------
# if "token" not in st.session_state:
#     st.session_state.token = None

# st.set_page_config(page_title="JWT Auth Prediction App", layout="centered")
# st.title("🔐 JWT Authentication + Prediction")

# # ---------------- AUTH SECTION ----------------
# st.subheader("Register / Login")

# tab1, tab2 = st.tabs(["Register", "Login"])

# with tab1:
#     reg_username = st.text_input("Username", key="reg_user")
#     reg_password = st.text_input("Password", type="password", key="reg_pass")

#     if st.button("Register"):
#         payload = {
#             "username": reg_username,
#             "password": reg_password
#         }
#         res = requests.post(f"{BASE_URL}/register", json=payload)

#         if res.status_code == 200:
#             data = res.json()
#             st.session_state.token = data["access_token"]
#             st.success("Registered successfully 🎉")
#         else:
#             st.error(res.json()["detail"])

# with tab2:
#     login_username = st.text_input("Username", key="login_user")
#     login_password = st.text_input("Password", type="password", key="login_pass")

#     if st.button("Login"):
#         payload = {
#             "username": login_username,
#             "password": login_password
#         }
#         res = requests.post(f"{BASE_URL}/login", json=payload)

#         if res.status_code == 200:
#             data = res.json()
#             st.session_state.token = data["access_token"]
#             st.success("Logged in successfully ✅")
#         else:
#             st.error(res.json()["detail"])

# # ---------------- PREDICTION SECTION ----------------
# st.divider()
# st.subheader("🔮 Prediction (Protected Route)")

# if st.session_state.token is None:
#     st.warning("Please login first to access prediction.")
# else:
#     st.success("Authenticated ✔️")

#     # -------- CUSTOMER DATA (MATCH YOUR CustomerData MODEL) --------
#     age = st.number_input("Age", min_value=1, max_value=100)
#     income = st.number_input("Income", min_value=0)
#     loan_amount = st.number_input("Loan Amount", min_value=0)
#     credit_score = st.number_input("Credit Score", min_value=300, max_value=900)

#     if st.button("Predict"):
#         payload = {
#             "customer": {
#                 "age": age,
#                 "income": income,
#                 "loan_amount": loan_amount,
#                 "credit_score": credit_score
#             }
#         }

#         headers = {
#             "Authorization": f"Bearer {st.session_state.token}"
#         }

#         res = requests.post(
#             f"{BASE_URL}/predict/auth",
#             json=payload,
#             headers=headers
#         )

#         if res.status_code == 200:
#             st.success("Prediction Successful 🎯")
#             st.json(res.json())
#         else:
#             st.error(res.json())

import streamlit as st
import requests

# ---------------- CONFIG ----------------
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Churn Prediction App", layout="centered")
st.title("🔐 Customer Churn Prediction (JWT Protected)")

# ---------------- SESSION ----------------
if "token" not in st.session_state:
    st.session_state.token = None

# ---------------- AUTH ----------------
st.subheader("Authentication")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        res = requests.post(
            f"{BASE_URL}/login",
            json={"username": username, "password": password}
        )
        if res.status_code == 200:
            st.session_state.token = res.json()["access_token"]
            st.success("Logged in successfully ✅")
        else:
            st.error(res.json()["detail"])

with tab2:
    r_username = st.text_input("Username", key="reg_user")
    r_password = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Register"):
        res = requests.post(
            f"{BASE_URL}/register",
            json={"username": r_username, "password": r_password}
        )
        if res.status_code == 200:
            st.session_state.token = res.json()["access_token"]
            st.success("Registered successfully 🎉")
        else:
            st.error(res.json()["detail"])

# ---------------- PREDICTION ----------------
st.divider()
st.subheader("📊 Customer Details")

if st.session_state.token is None:
    st.warning("Please login to make a prediction.")
else:
    # -------- INPUTS (MATCH PKL MODEL COLUMNS) --------
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=18, max_value=100)
    tenure = st.number_input("Tenure (months)", min_value=0)
    services = st.number_input("Services Subscribed", min_value=0)
    contract = st.selectbox(
        "Contract Type",
        ["Month-to-month", "One year", "Two year"]
    )
    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.01,
        step=0.01
    )

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.01,
        step=0.01
    )

    tech_support = st.selectbox("Tech Support", ["Yes", "No"])
    online_security = st.selectbox("Online Security", ["Yes", "No"])
    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    if st.button("🔮 Predict Churn"):
        payload = {
            "customer": {
                "Gender": gender,
                "Age": age,
                "Tenure": tenure,
                "Services_Subscribed": services,
                "Contract_Type": contract,
                "MonthlyCharges": monthly_charges,
                "TotalCharges": total_charges,
                "TechSupport": tech_support,
                "OnlineSecurity": online_security,
                "InternetService": internet_service
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
            st.success("Prediction successful 🎯")
            st.json(res.json())
        else:
            st.error(res.json())

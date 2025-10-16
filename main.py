import streamlit as st
from streamlit_lottie import st_lottie
import json
from prediction_helper import predict

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="ML for Premium Prediction", page_icon="💊", layout="wide", initial_sidebar_state="expanded")


# ---------- Utility ----------
def load_lottie(path: str):
    with open(path, "r") as f:
        return json.load(f)


# ---------- Load Animations ----------
animations = {
    "demographics": load_lottie("animations/demographics.json"),
    "health": load_lottie("animations/health.json"),
    "lifestyle": load_lottie("animations/lifestyle.json"),
    "plan": load_lottie("animations/plan.json"),
    "predict": load_lottie("animations/predict.json"),
}

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 💡 About This Project")
    st.write(
        """
        This project represents my **machine learning journey** into predictive modeling within the healthcare domain.  

        The model behind this app is a **hybrid ML pipeline** that combines both **Linear Regression** and **XGBoost** algorithms — leveraging the interpretability of linear models with the predictive strength of gradient boosting to achieve **higher accuracy across all data ranges**.

        During experimentation, I focused on:
        - Extensive **data cleaning and feature engineering** to handle skewed health and income data.  
        - Using libraries like **Pandas**, **NumPy**, **Scikit-learn**, and **XGBoost** for preprocessing, model training, and optimization.  
        - Performing **cross-validation**, **hyperparameter tuning**, and **error analysis** to minimize bias and variance.  

        This project aims to **make health insurance cost prediction more transparent** — helping users understand how their **age, health conditions, and lifestyle** affect premium pricing.  

        It’s a step toward **data-driven decision-making in healthcare** and improving **fairness and personalization** in premium estimation.
        """
    )
    st.markdown("---")
    st.markdown("👨‍💻 *Developed by Samarth Goswami*")

# ---------- Header with logo ----------
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("logo.png", width=290)
with col_title:
    st.markdown("<h2 style='font-weight:700;'>Health Insurance Cost Predictor</h2>", unsafe_allow_html=True)
    st.write(
        "A guided 5-step journey to predict your health insurance premium — powered by machine learning. "
        "This app analyzes your demographics, health, lifestyle, and plan preferences to estimate your personalized premium in seconds promising a 98% accuracy."
    )

st.divider()

# ---------- Wizard State ----------
if "step" not in st.session_state:
    st.session_state.step = 1
if "answers" not in st.session_state:
    st.session_state.answers = {}


def next_step(): st.session_state.step += 1


def prev_step(): st.session_state.step = max(1, st.session_state.step - 1)


# ---------- Step Progress ----------
st.progress((st.session_state.step - 1) / 4)

# ---------- DEMOGRAPHICS ----------
if st.session_state.step == 1:
    col_anim, col_form = st.columns([1, 2])
    with col_anim:
        st_lottie(animations["demographics"], height=220)
    with col_form:
        st.subheader("Step 1 — Demographics")
        age = st.number_input("Age", 18, 100)
        dependants = st.number_input("Dependants", 0, 10)
        gender = st.selectbox("Gender", ["Male", "Female"])
        marital = st.selectbox("Marital Status", ["Married", "Unmarried"])
        region = st.selectbox("Region", ["Northwest", "Southeast", "Northeast", "Southwest"])
        if st.button("Next ️", use_container_width=True):
            st.session_state.answers.update({
                "Age": age,
                "Number of Dependants": dependants,
                "Gender": gender,
                "Marital Status": marital,
                "Region": region
            })
            next_step()

# ---------- HEALTH ----------
elif st.session_state.step == 2:
    col_anim, col_form = st.columns([1, 2])
    with col_anim:
        st_lottie(animations["health"], height=220)
    with col_form:
        st.subheader("Step 2 — Health")
        bmi = st.selectbox("BMI Category", ["Normal", "Obesity", "Overweight", "Underweight"])
        history = st.selectbox(
            "Medical History", [
                'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
                'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
                'Diabetes & Heart disease'
            ])
        genetical = st.slider("Genetical Risk (0–5)", 0, 5, 1)
        col_btn = st.columns(2)
        if col_btn[0].button("Back", use_container_width=True): prev_step()
        if col_btn[1].button("Next", use_container_width=True):
            st.session_state.answers.update({
                "BMI Category": bmi,
                "Medical History": history,
                "Genetical Risk": genetical
            })
            next_step()

# ---------- LIFESTYLE ----------
elif st.session_state.step == 3:
    col_anim, col_form = st.columns([1, 2])
    with col_anim:
        st_lottie(animations["lifestyle"], height=220)
    with col_form:
        st.subheader("Step 3 — Lifestyle")
        smoking = st.selectbox("Smoking Status", ["No Smoking", "Regular", "Occasional"])
        job = st.selectbox("Employment Status", ["Salaried", "Self-Employed", "Freelancer"])
        income = st.number_input("Income in US Dollar", 0, 200000)
        col_btn = st.columns(2)
        if col_btn[0].button("Back", use_container_width=True): prev_step()
        if col_btn[1].button("Next ️", use_container_width=True):
            st.session_state.answers.update({
                "Smoking Status": smoking,
                "Employment Status": job,
                "Income in Lakhs": income
            })
            next_step()

# ---------- PLAN ----------
elif st.session_state.step == 4:
    col_anim, col_form = st.columns([1, 2])
    with col_anim:
        st_lottie(animations["plan"], height=220)
    with col_form:
        st.subheader("Step 4 — Plan Details")
        plan = st.selectbox("Insurance Plan", ["Bronze", "Silver", "Gold"])
        col_btn = st.columns(2)
        if col_btn[0].button("Back", use_container_width=True): prev_step()
        if col_btn[1].button("Next ️", use_container_width=True):
            st.session_state.answers["Insurance Plan"] = plan
            next_step()

# ---------- PREDICT ----------
elif st.session_state.step == 5:
    col_anim, col_form = st.columns([1, 2])
    with col_anim:
        st_lottie(animations["predict"], height=220)
    with col_form:
        st.subheader("✅ Step 5 — Review & Predict")
        st.write("### Summary")
        st.table(st.session_state.answers)
        col_btn = st.columns(2)
        if col_btn[0].button("Back", use_container_width=True): prev_step()
        if col_btn[1].button("Predict Now", use_container_width=True):
            with st.spinner("Calculating your premium..."):
                try:
                    pred = predict(st.session_state.answers)
                    st.success(f"💰 **Predicted Health Insurance Cost:** $ {pred:,}")
                except Exception as e:
                    st.error(f"Prediction failed: {e}")

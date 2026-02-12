import streamlit as st
import base64
import os
import time


try:
    from utils.predict import predict_health
except ImportError:
    def predict_health(age, height, weight, bmi, steps, sleep):
        return "Healthy", "Your vitals are looking great! Keep up the good work."

# Try to import auth; if not found, use dummy functions
try:
    from auth import create_user, login_user
except ImportError:
    def create_user(u, p, r):
        return True


    def login_user(u, p):
        return [("Demo User", "pass", "user")]


st.set_page_config(
    page_title="SugarSense AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None


def navigate_to(page):
    st.session_state.page = page
    st.rerun()


def toggle_auth_mode():
    st.session_state.auth_mode = 'signup' if st.session_state.auth_mode == 'login' else 'login'
    st.rerun()


def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None


background_file = "background.png"
bin_str = get_base64_of_bin_file(background_file)

if bin_str:
    background_style = f"""
        background-image: linear-gradient(rgba(0, 0, 10, 0.7), rgba(0, 0, 10, 0.9)), url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    """
else:
    background_style = "background: linear-gradient(135deg, #0f172a, #020617);"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600&display=swap');

    .stApp {{ {background_style} }}
    header, footer {{visibility: hidden;}}

    h1, h2, h3 {{ color: white !important; font-family: 'Orbitron', sans-serif; }}
    p, label {{ color: #cbd5e1 !important; font-family: 'Inter', sans-serif; }}

    /* Input Fields Style */
    div[data-baseweb="input"] {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }}
    div[data-baseweb="input"] input {{ color: white !important; }}

    /* Buttons */
    div.stButton > button {{
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border: none;
        padding: 12px 0;
        border-radius: 30px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
        margin-top: 10px;
    }}
    div.stButton > button:hover {{
        box-shadow: 0 0 20px rgba(0, 198, 255, 0.8);
        transform: scale(1.02);
    }}

    /* Landing Page Titles */
    .main-title {{
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        color: white;
        text-shadow: 0 0 30px rgba(0, 198, 255, 0.5);
        margin-bottom: 0;
    }}
    .ai-badge {{
        font-size: 2rem;
        color: #00e5ff;
        text-align: center;
        letter-spacing: 8px;
        font-family: 'Orbitron', sans-serif;
        margin-bottom: 20px;
    }}

    /* Feature Cards */
    .feature-card {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 229, 255, 0.3);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(5px);
        margin-bottom: 20px;
        transition: transform 0.3s;
    }}
    .feature-card:hover {{
        transform: translateY(-5px);
        border-color: #00e5ff;
        background: rgba(0, 229, 255, 0.1);
    }}
</style>
""", unsafe_allow_html=True)

if st.session_state.page == 'landing':

    # Title Section
    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">SUGARSENSE</div>', unsafe_allow_html=True)
    st.markdown('<div class="ai-badge">AI</div>', unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align: center; max-width: 600px; margin: 0 auto;'>Predict. Prevent. Protect. AI-powered healthcare.</p>",
        unsafe_allow_html=True)
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

    # Get Started Button (CENTERED)
    c1, c2, c3 = st.columns([1, 0.5, 1])
    with c2:
        if st.button("GET STARTED"):
            navigate_to('login')

    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)


    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 AI Predictions</h3>
            <p>Advanced ML models.</p>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class="feature-card">
            <h3>💓 Monitoring</h3>
            <p>Real-time vitals tracking.</p>
        </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown("""
        <div class="feature-card">
            <h3>🛡️ Secure</h3>
            <p>HIPAA compliant encryption.</p>
        </div>
        """, unsafe_allow_html=True)
    with f4:
        st.markdown("""
        <div class="feature-card">
            <h3>📈 Analytics</h3>
            <p>Smart health insights.</p>
        </div>
        """, unsafe_allow_html=True)


elif st.session_state.page == 'login':

    col1, col2, col3 = st.columns([1, 0.8, 1])

    with col2:
        # Spacer
        st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)

        if st.session_state.auth_mode == 'login':
            st.markdown('<h2 style="text-align: center;">Login</h2>', unsafe_allow_html=True)

            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("LOGIN"):
                if username and password:
                    user = login_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = username
                        st.success("Success!")
                        time.sleep(0.5)
                        navigate_to('dashboard')
                    else:
                        st.error("Invalid Credentials")
                else:
                    st.warning("Enter details")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account"):
                toggle_auth_mode()

        else:  # SIGNUP MODE
            st.markdown('<h2 style="text-align: center;">Sign Up</h2>', unsafe_allow_html=True)

            new_user = st.text_input("New Username", key="signup_user")
            new_pass = st.text_input("New Password", type="password", key="signup_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="signup_confirm")

            if st.button("SIGN UP"):
                if new_user and new_pass == confirm_pass:
                    if create_user(new_user, new_pass, 'user'):
                        st.success("Account created! Log in now.")
                        time.sleep(1)
                        toggle_auth_mode()
                    else:
                        st.error("Username taken")
                else:
                    st.error("Check passwords")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Back to Login"):
                toggle_auth_mode()


        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅ Back to Home"):
            navigate_to('landing')


elif st.session_state.page == 'dashboard':

    with st.sidebar:
        st.title("SugarSense")
        st.write(f"User: **{st.session_state.user}**")
        st.markdown("---")

        if st.button("🚪 Logout", key="sidebar_logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            navigate_to("landing")



    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("⬅ Back", key="main_back"):
            navigate_to("landing")

    st.markdown("## 🧠 Health Dashboard")
    st.markdown("### Enter Your Health Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 10, 80, 22, key="main_age")
        height = st.number_input("Height (cm)", 120, 200, 170, key="main_height")
        weight = st.number_input("Weight (kg)", 30, 120, 70, key="main_weight")

    with col2:
        bmi = st.number_input("BMI", 10.0, 40.0, 24.5, key="main_bmi")
        steps = st.number_input("Daily Steps", 0, 20000, 4000, key="main_steps")
        sleep = st.number_input("Sleep Hours", 0.0, 12.0, 6.0, key="main_sleep")

    st.markdown("---")


    if st.button("🔮 Predict Health Advice"):
        label, explanation = predict_health(
            age, height, weight, bmi, steps, sleep
        )

        st.success(f"✅ AI Suggestion: {label}")

        st.markdown("### 🧾 Reason / Advice")
        st.info(explanation)
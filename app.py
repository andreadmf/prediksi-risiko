import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
import time

# ==========================================
# 1. MENYIAPKAN DATA HISTORIS
# ==========================================

X_train = np.array([
    [5, 10],
    [10, 20],
    [15, 5],
    [20, 25],
    [25, 15]
])

y_train = np.array([50, 80, 110, 90, 150])

# ==========================================
# 2. MELATIH MODEL
# ==========================================

model = LinearRegression()
model.fit(X_train, y_train)

baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]

# ==========================================
# 3. FUNGSI SIMULASI
# ==========================================

def run_simulation(new_iklan, new_diskon):
    intervention_input = np.array([[new_iklan, new_diskon]])
    prediction = model.predict(intervention_input)[0]
    delta_y = prediction - baseline_pred
    return prediction, delta_y

# ==========================================
# 4. SESSION STATE INITIALIZATION
# ==========================================

if 'simulation_history' not in st.session_state:
    st.session_state.simulation_history = []

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

if 'user_name' not in st.session_state:
    st.session_state.user_name = "User"

if 'last_confetti' not in st.session_state:
    st.session_state.last_confetti = 0

# ==========================================
# 5. PAGE CONFIG & CUSTOM CSS
# ==========================================

st.set_page_config(
    page_title="🎮 Profit Simulator Pro",
    layout="wide",
    page_icon="🎯"
)

st.markdown("""
<style>
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        padding: 2rem;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }

    /* Metric Cards */
    .stMetric {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    .stMetric [data-testid="stMetricLabel"] p {
        color: #1a1a1a !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #1a1a1a !important;
    }

    /* Sidebar */
    .css-1d391kg {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 15px !important;
    }

    /* Headings */
    h1, h2, h3 {
        color: white !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5) !important;
        font-weight: bold !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    }

    /* Chat Messages */
    .chat-message {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 10px 15px !important;
        border-radius: 15px !important;
        margin: 5px 0 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3) !important;
        color: #1a1a1a !important;
    }
    .chat-message * {
        color: #1a1a1a !important;
    }

    /* History Cards */
    .history-card {
        background: rgba(255,255,255,0.98) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.3) !important;
        color: #1a1a1a !important;
    }
    .history-card * {
        color: #1a1a1a !important;
    }

    /* All Text in Markdown Containers */
    div[data-testid="stMarkdownContainer"] p {
        color: white !important;
    }
    div[data-testid="stMarkdownContainer"] {
        color: white !important;
    }

    /* Labels */
    label {
        color: white !important;
    }

    /* DataFrames & Charts */
    [data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }

    /* Info/Warning/Success Boxes */
    .stAlert {
        background: rgba(255,255,255,0.95) !important;
        color: #1a1a1a !important;
    }
    .stAlert * {
        color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 6. HEADER
# ==========================================

st.markdown("""
<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 20px; margin-bottom: 20px;">
""", unsafe_allow_html=True)
st.title("🎮 Profit Simulator Pro")
st.subheader("🔮 Digital Twin What-If Analysis")
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 7. SIDEBAR
# ==========================================

st.sidebar.header("⚙️ Controls")

st.sidebar.text_input("👤 Your Name", value=st.session_state.user_name, key="user_name_input")
st.session_state.user_name = st.session_state.user_name_input

iklan_slider = st.sidebar.slider(
    "📢 Ad Budget (Million)",
    min_value=0,
    max_value=50,
    value=10
)

diskon_slider = st.sidebar.slider(
    "🏷️ Discount (%)",
    min_value=0,
    max_value=50,
    value=10
)

if st.sidebar.button("🎯 Save Simulation"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    pred, delta = run_simulation(iklan_slider, diskon_slider)
    st.session_state.simulation_history.append({
        "time": timestamp,
        "ad_budget": iklan_slider,
        "discount": diskon_slider,
        "profit": pred,
        "delta": delta
    })
    st.sidebar.success("✅ Simulation saved!")

if st.sidebar.button("🗑️ Clear History"):
    st.session_state.simulation_history = []
    st.sidebar.warning("History cleared!")

# ==========================================
# 8. RUN SIMULATION
# ==========================================

hasil_prediksi, delta = run_simulation(iklan_slider, diskon_slider)

# Confetti animation
if delta > 0 and (time.time() - st.session_state.last_confetti > 3):
    st.balloons()
    st.session_state.last_confetti = time.time()

# ==========================================
# 9. METRICS
# ==========================================

col1, col2, col3 = st.columns(3)
emoji = "🚀" if delta > 0 else "📉" if delta < 0 else "⏸️"
delta_color = "#2ecc71" if delta > 0 else "#e74c3c" if delta < 0 else "#95a5a6"

with col1:
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.98) !important; border-radius: 15px !important; padding: 20px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;">
        <p style="color: #1a1a1a !important; font-size: 16px !important; margin: 0 0 10px 0 !important;">💰 Predicted Profit</p>
        <p style="color: #1a1a1a !important; font-size: 28px !important; font-weight: bold !important; margin: 0 0 5px 0 !important;">Rp {hasil_prediksi:.2f}M</p>
        <p style="color: {delta_color} !important; font-size: 18px !important; margin: 0 !important;">{'↑' if delta > 0 else '↓' if delta < 0 else ''} {delta:.2f}M</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.98) !important; border-radius: 15px !important; padding: 20px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;">
        <p style="color: #1a1a1a !important; font-size: 16px !important; margin: 0 0 10px 0 !important;">📊 Baseline</p>
        <p style="color: #1a1a1a !important; font-size: 28px !important; font-weight: bold !important; margin: 0 !important;">Rp {baseline_pred:.2f}M</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.98) !important; border-radius: 15px !important; padding: 20px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;">
        <p style="color: #1a1a1a !important; font-size: 16px !important; margin: 0 0 10px 0 !important;">Status</p>
        <p style="font-size: 40px !important; margin: 0 !important;">{emoji}</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 10. SCENARIO ANALYSIS
# ==========================================

st.markdown(f'<h2 style="color: white !important; text-shadow: 3px 3px 6px rgba(0,0,0,0.5) !important;">📈 Scenario Analysis</h2>', unsafe_allow_html=True)

if delta > 0:
    st.markdown(f"""
    <div style="background: rgba(46, 204, 113, 0.95) !important; color: white !important; padding: 15px !important; border-radius: 10px !important; margin: 10px 0 !important;">
        <p style="color: white !important; font-size: 16px !important; margin: 0 !important;">🎉 Excellent! Profit increases by {delta:.2f}M!</p>
    </div>
    """, unsafe_allow_html=True)
elif delta < 0:
    st.markdown(f"""
    <div style="background: rgba(231, 76, 60, 0.95) !important; color: white !important; padding: 15px !important; border-radius: 10px !important; margin: 10px 0 !important;">
        <p style="color: white !important; font-size: 16px !important; margin: 0 !important;">⚠️ Warning: Profit decreases by {abs(delta):.2f}M</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style="background: rgba(52, 152, 219, 0.95) !important; color: white !important; padding: 15px !important; border-radius: 10px !important; margin: 10px 0 !important;">
        <p style="color: white !important; font-size: 16px !important; margin: 0 !important;">ℹ️ No change from baseline</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 11. CHARTS
# ==========================================

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown(f'<h2 style="color: white !important; text-shadow: 3px 3px 6px rgba(0,0,0,0.5) !important;">📊 Delta Analysis</h2>', unsafe_allow_html=True)
    data_delta = pd.DataFrame({
        "Scenario": ["Baseline", "Current"],
        "Profit": [baseline_pred, hasil_prediksi]
    })
    st.bar_chart(data=data_delta, x="Scenario", y="Profit")

with col_chart2:
    st.markdown(f'<h2 style="color: white !important; text-shadow: 3px 3px 6px rgba(0,0,0,0.5) !important;">📉 History Trend</h2>', unsafe_allow_html=True)
    if len(st.session_state.simulation_history) > 0:
        hist_df = pd.DataFrame(st.session_state.simulation_history)
        hist_df["index"] = range(1, len(hist_df)+1)
        st.line_chart(data=hist_df, x="index", y="profit")

# ==========================================
# 12. SIMULATION HISTORY
# ==========================================

st.markdown("""
<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 20px; margin: 20px 0;">
""", unsafe_allow_html=True)
st.markdown(f'<h2 style="color: white !important; text-shadow: 3px 3px 6px rgba(0,0,0,0.5) !important;">📜 Simulation History</h2>', unsafe_allow_html=True)
if len(st.session_state.simulation_history) > 0:
    for idx, sim in enumerate(reversed(st.session_state.simulation_history[-5:])):
        with st.container():
            st.markdown(f"""
            <div class="history-card">
                <b>🕐 {sim['time']}</b> | Ad: {sim['ad_budget']}M | Discount: {sim['discount']}%<br>
                💰 Profit: Rp {sim['profit']:.2f}M | Δ: {sim['delta']:.2f}M
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No simulations saved yet. Use the sidebar to save!")
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 13. ONLINE CHAT MODE
# ==========================================

st.markdown("""
<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 20px; margin: 20px 0;">
""", unsafe_allow_html=True)
st.markdown(f'<h2 style="color: white !important; text-shadow: 3px 3px 6px rgba(0,0,0,0.5) !important;">💬 Live Chat (Online Mode)</h2>', unsafe_allow_html=True)

chat_col1, chat_col2 = st.columns([3, 1])

with chat_col1:
    chat_message = st.text_input("Type your message...", key="chat_input")

with chat_col2:
    if st.button("Send 📨"):
        if chat_message:
            st.session_state.chat_messages.append({
                "user": st.session_state.user_name,
                "time": datetime.now().strftime("%H:%M:%S"),
                "message": chat_message
            })

# Display chat
for msg in st.session_state.chat_messages[-10:]:
    st.markdown(f"""
    <div class="chat-message">
        <b>{msg['user']}</b> <small>({msg['time']})</small><br>
        {msg['message']}
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 14. FOOTER
# ==========================================

st.markdown("---")
st.caption(
    "🎯 Praktikum Pemodelan & Simulasi - Tugas 14 | Made with ❤️ & Unique Features!"
)
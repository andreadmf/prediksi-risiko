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
    page_title="🎮 Simulator Keuntungan Pro",
    layout="wide",
    page_icon="🎯"
)

st.markdown("""
<style>
    .main, .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 6. HEADER
# ==========================================

st.markdown("""
<h1 style="color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); font-weight: bold; margin: 0;">🎮 Simulator Kebijakan Keuntungan</h1>
<h2 style="color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); font-weight: bold; margin-top: 10px;">🔮 Digital Twin What-If Analysis</h2>
""", unsafe_allow_html=True)

# ==========================================
# 7. SIDEBAR
# ==========================================

st.sidebar.markdown("""
<h3 style="color: #1a1a1a; font-weight: bold; margin: 0 0 15px 0;">⚙️ Kontrol</h3>
""", unsafe_allow_html=True)

# Sidebar Name Input
name_input = st.sidebar.text_input("👤 Nama Kamu", value=st.session_state.user_name, key="user_name_input")
st.session_state.user_name = name_input

# Sidebar Sliders
iklan_slider = st.sidebar.slider(
    "📢 Anggaran Iklan (Juta)",
    min_value=0,
    max_value=50,
    value=10
)

diskon_slider = st.sidebar.slider(
    "🏷️ Diskon (%)",
    min_value=0,
    max_value=50,
    value=10
)

# Sidebar Buttons
if st.sidebar.button("🎯 Simpan Simulasi"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    pred, delta = run_simulation(iklan_slider, diskon_slider)
    st.session_state.simulation_history.append({
        "time": timestamp,
        "ad_budget": iklan_slider,
        "discount": diskon_slider,
        "profit": pred,
        "delta": delta
    })
    st.sidebar.markdown("""
    <div style="background: rgba(46, 204, 113, 0.2); color: #1a1a1a; padding: 10px; border-radius: 10px; margin-top: 10px;">
        ✅ Simulasi berhasil disimpan!
    </div>
    """, unsafe_allow_html=True)

if st.sidebar.button("🗑️ Hapus Riwayat"):
    st.session_state.simulation_history = []
    st.sidebar.markdown("""
    <div style="background: rgba(241, 196, 15, 0.2); color: #1a1a1a; padding: 10px; border-radius: 10px; margin-top: 10px;">
        ⚠️ Riwayat telah dihapus!
    </div>
    """, unsafe_allow_html=True)

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
    <div style="background: rgba(255,255,255,0.98); border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <p style="color: #1a1a1a; font-size: 16px; margin: 0 0 10px 0;">💰 Predicted Profit</p>
        <p style="color: #1a1a1a; font-size: 28px; font-weight: bold; margin: 0 0 5px 0;">Rp {hasil_prediksi:.2f}M</p>
        <p style="color: {delta_color}; font-size: 18px; margin: 0;">{'↑' if delta > 0 else '↓' if delta < 0 else ''} {delta:.2f}M</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.98); border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <p style="color: #1a1a1a; font-size: 16px; margin: 0 0 10px 0;">📊 Baseline</p>
        <p style="color: #1a1a1a; font-size: 28px; font-weight: bold; margin: 0;">Rp {baseline_pred:.2f}M</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.98); border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <p style="color: #1a1a1a; font-size: 16px; margin: 0 0 10px 0;">Status</p>
        <p style="font-size: 40px; margin: 0;">{emoji}</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 10. SCENARIO ANALYSIS
# ==========================================

st.markdown("""
<h3 style="color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); font-weight: bold; margin-top: 30px;">📈 Analisis Skenario</h3>
""", unsafe_allow_html=True)

if delta > 0:
    st.markdown(f"""
    <div style="background: rgba(46, 204, 113, 0.2); color: #1a1a1a; padding: 15px; border-radius: 10px; margin-top: 10px;">
        🎉 Bagus! Keuntungan naik sebesar Rp {delta:.2f} Juta!
    </div>
    """, unsafe_allow_html=True)
elif delta < 0:
    st.markdown(f"""
    <div style="background: rgba(231, 76, 60, 0.2); color: #1a1a1a; padding: 15px; border-radius: 10px; margin-top: 10px;">
        ⚠️ Perhatian! Keuntungan turun sebesar Rp {abs(delta):.2f} Juta
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background: rgba(52, 152, 219, 0.2); color: #1a1a1a; padding: 15px; border-radius: 10px; margin-top: 10px;">
        ℹ️ Tidak ada perubahan dari baseline
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 11. CHARTS
# ==========================================

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("""
    <h3 style="color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); font-weight: bold; margin-top: 30px;">📊 Analisis Delta</h3>
    """, unsafe_allow_html=True)
    data_delta = pd.DataFrame({
        "Skenario": ["Baseline", "Saat Ini"],
        "Keuntungan": [baseline_pred, hasil_prediksi]
    })
    st.bar_chart(data=data_delta, x="Skenario", y="Keuntungan")

with col_chart2:
    st.markdown("""
    <h3 style="color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); font-weight: bold; margin-top: 30px;">📉 Tren Riwayat</h3>
    """, unsafe_allow_html=True)
    if len(st.session_state.simulation_history) > 0:
        hist_df = pd.DataFrame(st.session_state.simulation_history)
        hist_df["index"] = range(1, len(hist_df)+1)
        st.line_chart(data=hist_df, x="index", y="profit")

# ==========================================
# 12. SIMULATION HISTORY
# ==========================================

st.markdown("""
<div style="margin-top: 30px;">
    <h3 style="color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); font-weight: bold; margin: 0;">📜 Riwayat Simulasi</h3>
</div>
""", unsafe_allow_html=True)

if len(st.session_state.simulation_history) > 0:
    for idx, sim in enumerate(reversed(st.session_state.simulation_history[-5:])):
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.98); border-radius: 10px; padding: 15px; margin: 10px 0; box-shadow: 0 3px 10px rgba(0,0,0,0.3); color: #1a1a1a;">
            <b>🕐 {sim['time']}</b> | Iklan: {sim['ad_budget']} Juta | Diskon: {sim['discount']}%<br>
            💰 Keuntungan: Rp {sim['profit']:.2f} Juta | Δ: {sim['delta']:.2f} Juta
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background: rgba(52, 152, 219, 0.2); color: #1a1a1a; padding: 15px; border-radius: 10px; margin-top: 10px;">
        ℹ️ Belum ada simulasi yang disimpan. Gunakan tombol di sidebar!
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 13. ONLINE CHAT MODE
# ==========================================

st.markdown("""
<div style="margin-top: 30px;">
    <h3 style="color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); font-weight: bold; margin: 0;">💬 Live Chat (Mode Online)</h3>
</div>
""", unsafe_allow_html=True)

chat_col1, chat_col2 = st.columns([3, 1])

with chat_col1:
    chat_message = st.text_input("Ketik pesan kamu...", key="chat_input")

with chat_col2:
    if st.button("Kirim 📨"):
        if chat_message:
            st.session_state.chat_messages.append({
                "user": st.session_state.user_name,
                "time": datetime.now().strftime("%H:%M:%S"),
                "message": chat_message
            })

# Display chat
for msg in st.session_state.chat_messages[-10:]:
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.98); padding: 10px 15px; border-radius: 15px; margin: 5px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.3); color: #1a1a1a;">
        <b>{msg['user']}</b> <small>({msg['time']})</small><br>
        {msg['message']}
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 14. FOOTER
# ==========================================

st.markdown("---")
st.caption(
    "🎯 Praktikum Pemodelan & Simulasi - Tugas 14 | Made with ❤️ & Unique Features!"
)
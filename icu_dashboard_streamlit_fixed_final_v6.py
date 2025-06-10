
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import ttest_ind
import gdown

# Set page config
st.set_page_config(page_title='ICU Dashboard', layout="wide")

# Force background color to black
st.markdown("""
<style>
    body {
        background-color: #1c1e29 !important;
    }
</style>
""", unsafe_allow_html=True)

# Download CSV from Google Drive
file_url = "https://drive.google.com/uc?id=1CvjJObXyhuLX5ElQ9PStpXx6rYQWPPpC"
output = "training_v2.csv"
gdown.download(file_url, output, quiet=False)

# Load data
data = pd.read_csv(output)

# Toggle theme
is_dark = st.checkbox("🌙 Dark Mode", value=True)
bg_color = "#1c1e29" if is_dark else "#FFFFFF"
paper_color = "#1c1e29" if is_dark else "#FFFFFF"
font_color = "#f0f4f8" if is_dark else "#000000"
box_color = "#252934" if is_dark else "#F0F0F0"

# Category definitions
categories = {
    '🩸 בדיקת דם': {
        'albumin_apache': 'רמת אלבומין (תפקוד תזונתי וכבד)',
        'bilirubin_apache': 'רמת בילירובין (תפקודי כבד)',
        'bun_apache': 'חנקן אוריאה בדם (תפקוד כלייתי)',
        'creatinine_apache': 'רמת קריאטינין (תפקוד כלייתי)',
        'glucose_apache': 'רמת גלוקוז (סוכר בדם)',
        'hematocrit_apache': 'אחוז המטוקריט (נפח כדוריות דם אדומות)',
        'sodium_apache': 'רמת נתרן (איזון אלקטרוליטים)',
        'wbc_apache': 'ספירת תאי דם לבנים (סמן לזיהום או דלקת)'
    },
    '🌡️ Vital Signs': {
        'heart_rate_apache': 'דופק לב (קצב פעימות הלב)',
        'map_apache': 'לחץ דם עורקי ממוצע',
        'resprate_apache': 'קצב הנשימות לדקה',
        'temp_apache': 'טמפרטורת הגוף',
        'urineoutput_apache': 'תפוקת השתן (תפקוד כלייתי ונוזלים)'
    },
    '🫁 Respiration and Oxygenation': {
        'fio2_apache': 'אחוז חמצן המסופק למטופל (חמצון מלאכותי)',
        'intubated_apache': 'האם המטופל מונשם (כן או לא)',
        'ventilated_apache': 'האם המטופל מחובר למכונת הנשמה (כן או לא)',
        'paco2_apache': 'לחץ חלקי של פחמן דו-חמצני בדם עורקי',
        'paco2_for_ph_apache': 'לחץ חלקי של CO₂ לצורך חישוב רמת חומציות (pH)',
        'pao2_apache': 'לחץ חלקי של חמצן בדם עורקי',
        'ph_apache': 'חומציות הדם (איזון חומצה-בסיס)'
    },
    '🧠 Neurological (GCS)': {
        'gcs_eyes_apache': 'תגובה של עיניים (בסולם גלזגו)',
        'gcs_motor_apache': 'תגובה מוטורית (תנועתית)',
        'gcs_verbal_apache': 'תגובה מילולית',
        'gcs_unable_apache': 'האם לא ניתן למדוד הכרה (כן או לא)'
    }
}

# Title centered
st.markdown(f"""
<div style='text-align:center;'>
<h1 style='color:#f39c12; font-size:36px;'>🌡️ ICU Patient Analysis Dashboard 📊</h1>
</div>
""", unsafe_allow_html=True)

# Dropdowns aligned horizontally
st.markdown("<div style='display:flex; justify-content:center; gap:20px;'>", unsafe_allow_html=True)
category = st.selectbox("Select Category", list(categories.keys()))
desc_to_var = {desc: var for var, desc in categories[category].items()}
selected_desc = st.selectbox("Select Variable", list(desc_to_var.keys()))
selected_var = desc_to_var[selected_desc]
st.markdown("</div>", unsafe_allow_html=True)

# Data filtering
df = data[['hospital_death', selected_var]].dropna()
survived = df[df['hospital_death'] == 0][selected_var]
died = df[df['hospital_death'] == 1][selected_var]

# T-Test
t_stat, p_value = ttest_ind(survived, died, equal_var=False)
significant = '✅ Yes' if p_value < 0.05 else '❌ No'

# Plot
fig = go.Figure()
fig.add_trace(go.Histogram(x=survived, name='Survived', opacity=0.8, marker_color='#00c853'))
fig.add_trace(go.Histogram(x=died, name='Died', opacity=0.8, marker_color='#ff5252'))
fig.update_layout(
    barmode='overlay',
    title=dict(text=f'<b>{selected_desc}</b>', font=dict(color=font_color)),
    plot_bgcolor=bg_color,
    paper_bgcolor=paper_color,
    font=dict(color=font_color),
    legend=dict(orientation='h', x=0.35, y=-0.15, font=dict(color=font_color))
)

# Show plot
st.plotly_chart(fig, use_container_width=True)

# Summary stats
summary_html = f'''<div style='text-align:center; font-size:20px; background-color:{box_color}; padding:20px; border-radius:12px; color:{font_color};'>
<b>🟢 Survived Mean</b>: {survived.mean():.2f}, <b>🔴 Died Mean</b>: {died.mean():.2f}, 
<b>🎯 P-Value</b>: {p_value:.4f}, <b>Statistically Significant</b>: {significant}
</div>'''
st.markdown(summary_html, unsafe_allow_html=True)


# Install first:
# !pip install streamlit plotly scipy pandas

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import ttest_ind

# Custom CSS to mimic Dash design
st.markdown("""
<style>
body {
    background-color: #1c1e29;
    color: #f0f4f8;
    font-family: Arial, sans-serif;
}
.css-18e3th9, .css-1d391kg {
    background-color: #1c1e29;
    color: #f0f4f8;
}
.css-1v0mbdj p {
    color: #f0f4f8;
}
div[data-baseweb="select"] > div {
    background-color: #ffffff;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# Read the data from Google Drive
file_id = "1CvjJObXyhuLX5ElQ9PStpXx6rYQWPPpC"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
data = pd.read_csv(url)

# Variables categorized with Hebrew descriptions
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

st.set_page_config(layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #f39c12; font-size: 36px;'>🌡️ ICU Patient Analysis Dashboard 📊</h1>",
    unsafe_allow_html=True
)

# Dropdowns
category = st.selectbox("בחר קטגוריה", list(categories.keys()))
variable_options = categories[category]
selected_var = st.selectbox("בחר משתנה", list(variable_options.keys()))
var_desc = variable_options[selected_var]

# Filter data
df = data[['hospital_death', selected_var]].dropna()
survived = df[df['hospital_death'] == 0][selected_var]
died = df[df['hospital_death'] == 1][selected_var]

# Stats
t_stat, p_value = ttest_ind(survived, died, equal_var=False)
significant = '✅ Yes' if p_value < 0.05 else '❌ No'

# Plot
fig = go.Figure()
fig.add_trace(go.Histogram(x=survived, name='Survived 🟢', opacity=0.8, marker_color='#00c853'))
fig.add_trace(go.Histogram(x=died, name='Died 🔴', opacity=0.8, marker_color='#ff5252'))
fig.update_layout(
    barmode='overlay',
    title=f"<b>{var_desc}</b>",
    plot_bgcolor='#1c1e29',
    paper_bgcolor='#1c1e29',
    font=dict(color='#f0f4f8'),
    legend=dict(orientation='h', x=0.35, y=-0.15)
)

# Styling containers
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    f"<div style='text-align: center; margin-top: 30px; font-size: 20px; background-color: #252934; padding: 20px; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.4); width: 85%; margin: auto;'>"
    f"🟢 Survived Mean: {survived.mean():.2f}, 🔴 Died Mean: {died.mean():.2f}, 🎯 P-Value: {p_value:.4f}, Significant: {significant}"
    f"</div>",
    unsafe_allow_html=True
)

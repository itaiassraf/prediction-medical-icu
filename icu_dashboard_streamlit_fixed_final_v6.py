import streamlit as st

# Set page layout
st.set_page_config(layout="wide")

# Toggle for dark mode
dark_mode = st.toggle("🌙 Dark Mode", value=True)

# Define color schemes
if dark_mode:
    bg_color = '#1c1e29'
    text_color = '#f0f4f8'
    box_color = '#252934'
    survived_color = '#00c853'
    died_color = '#ff5252'
else:
    bg_color = '#ffffff'
    text_color = '#1c1e29'
    box_color = '#f5f5f5'
    survived_color = '#66bb6a'
    died_color = '#ef5350'

import pandas as pd
import plotly.graph_objs as go
from scipy.stats import ttest_ind
import gdown

# Set page config
st.set_page_config(layout="wide")

# Download the CSV from Google Drive (public link)
file_url = "https://drive.google.com/uc?id=1CvjJObXyhuLX5ElQ9PStpXx6rYQWPPpC"
output = "training_v2.csv"
gdown.download(file_url, output, quiet=False)

# Load the dataset
data = pd.read_csv(output)

# Categories with Hebrew descriptions
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

# UI
st.title("🌡️ ICU Patient Analysis Dashboard 📊")
category = st.selectbox("בחר קטגוריה", list(categories.keys()))

# Reverse mapping from Hebrew description to variable
desc_to_var = {desc: var for var, desc in categories[category].items()}
selected_desc = st.selectbox("בחר משתנה", list(desc_to_var.keys()))
selected_var = desc_to_var[selected_desc]

# Filter data
df = data[['hospital_death', selected_var]].dropna()
survived = df[df['hospital_death'] == 0][selected_var]
died = df[df['hospital_death'] == 1][selected_var]

# t-test
t_stat, p_value = ttest_ind(survived, died, equal_var=False)
significant = '✅ כן' if p_value < 0.05 else '❌ לא'

# Plot
fig = go.Figure()
fig.add_trace(go.Histogram(x=survived, name='Survived', opacity=0.8, marker_color=survived_color))
fig.add_trace(go.Histogram(x=died, name='Died', opacity=0.8, marker_color=died_color))
fig.update_layout(
    barmode='overlay',
    title=dict(text=f'<b>{selected_desc}</b>', font=dict(color='#ffffff')),
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font=dict(color=text_color),
    legend=dict(
        orientation='h',
        x=0.35,
        y=-0.15,
        font=dict(color=text_color)
    )
)

# Display
st.plotly_chart(fig, use_container_width=True)
summary_html = f"""
<div style='text-align:center; font-size:20px; background-color:{box_color}; padding:20px; border-radius:12px; color:{text_color};'>
🟢 <b>Survived Mean</b>: {survived.mean():.2f}, 🔴 <b>Died Mean</b>: {died.mean():.2f}, 🎯 <b>P-Value</b>: {p_value:.4f}, <b>Statistically Significant</b>: {significant}
</div>
"""
    "<div style='text-align:center; font-size:20px; background-color:{box_color}; padding:20px; border-radius:12px; color:{text_color};'>"
    f"🟢 ממוצע שורדים: {survived.mean():.2f}, 🔴 ממוצע נפטרים: {died.mean():.2f}, 🎯 ערך-P: {p_value:.4f}, מובהקות סטטיסטית: {significant}"
    "</div>", unsafe_allow_html=True
st.markdown(summary_html, unsafe_allow_html=True)
)
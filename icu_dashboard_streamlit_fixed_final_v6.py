# Install first:
# pip install streamlit plotly scipy gdown

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import ttest_ind
import gdown

# Download the dataset from Google Drive (public link)
file_id = "1CvjJObXyhuLX5ElQ9PStpXx6rYQWPPpC"
gdown.download(f"https://drive.google.com/uc?id={file_id}", "training_v2.csv", quiet=False)

data = pd.read_csv("training_v2.csv")

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

# Toggle for dark mode
dark_mode = st.checkbox("🌙 Dark Mode", value=True)

# Style settings
bg_color = "#1c1e29" if dark_mode else "#ffffff"
font_color = "#f0f4f8" if dark_mode else "#000000"
card_bg = "#252934" if dark_mode else "#f5f5f5"

st.markdown(
    f"""
    <div style='background-color:{bg_color}; padding:30px; color:{font_color}; font-family:Arial, sans-serif'>
        <h1 style='text-align:center; color:#f39c12; font-size:36px;'>🌡️ ICU Patient Analysis Dashboard 📊</h1>
    </div>
    """,
    unsafe_allow_html=True
)

category = st.selectbox("בחר קטגוריה", list(categories.keys()))
variable_options = [{'label': desc, 'value': var} for var, desc in categories[category].items()]
selected_var = st.selectbox("בחר משתנה", variable_options, format_func=lambda x: x['label'])['value']

df = data[['hospital_death', selected_var]].dropna()
survived = df[df['hospital_death'] == 0][selected_var]
died = df[df['hospital_death'] == 1][selected_var]

# Statistics
t_stat, p_value = ttest_ind(survived, died, equal_var=False)
significant = '✅ Yes' if p_value < 0.05 else '❌ No'

# Graph
fig = go.Figure()
fig.add_trace(go.Histogram(x=survived, name='Survived 🟢', opacity=0.8, marker_color='#00c853'))
fig.add_trace(go.Histogram(x=died, name='Died 🔴', opacity=0.8, marker_color='#ff5252'))

fig.update_layout(
    barmode='overlay',
    title=f'<b>{[v for k, v in categories[category].items() if k == selected_var][0]}</b>',
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font=dict(color=font_color),
    legend=dict(orientation='h', x=0.35, y=-0.15, font=dict(color=font_color))
)

st.plotly_chart(fig, use_container_width=True)

# Stats display
st.markdown(
    f"""
    <div style='text-align:center; font-size:20px; background-color:{card_bg}; padding:20px; border-radius:12px; color:{font_color};'>
        🟢 Survived Mean: {survived.mean():.2f}, 🔴 Died Mean: {died.mean():.2f}, 🎯 P-Value: {p_value:.4f}, Significant: {significant}
    </div>
    """,
    unsafe_allow_html=True
)

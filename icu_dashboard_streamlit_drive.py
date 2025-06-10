# 📦 התקנות ראשוניות:
# !pip install streamlit plotly scipy pandas

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import ttest_ind

# קריאת הדאטה ישירות מה-Drive
file_id = "1CvjJObXyhuLX5ElQ9PStpXx6rYQWPPpC"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
data = pd.read_csv(url)

# קטגוריות ותיאורים בעברית
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
    '🌡️ סימנים חיוניים': {
        'heart_rate_apache': 'דופק לב (קצב פעימות הלב)',
        'map_apache': 'לחץ דם עורקי ממוצע',
        'resprate_apache': 'קצב הנשימות לדקה',
        'temp_apache': 'טמפרטורת הגוף',
        'urineoutput_apache': 'תפוקת השתן (תפקוד כלייתי ונוזלים)'
    },
    '🫁 נשימה וחמצון': {
        'fio2_apache': 'אחוז חמצן המסופק למטופל',
        'intubated_apache': 'האם המטופל מונשם',
        'ventilated_apache': 'האם המטופל מחובר למכונת הנשמה',
        'paco2_apache': 'לחץ CO₂ בדם עורקי',
        'paco2_for_ph_apache': 'CO₂ לחישוב pH',
        'pao2_apache': 'לחץ חמצן בדם עורקי',
        'ph_apache': 'חומציות הדם'
    },
    '🧠 נוירולוגיה (GCS)': {
        'gcs_eyes_apache': 'תגובה של עיניים',
        'gcs_motor_apache': 'תגובה מוטורית',
        'gcs_verbal_apache': 'תגובה מילולית',
        'gcs_unable_apache': 'לא ניתן למדוד הכרה'
    }
}

# כותרת
st.set_page_config(page_title="ICU Dashboard", layout="wide")
st.title("🌡️ דאשבורד לניתוח חולי טיפול נמרץ")

# קטגוריה
category = st.selectbox("בחר קטגוריה רפואית:", list(categories.keys()))

# משתנה
options = categories[category]
var_key = st.selectbox("בחר משתנה לניתוח:", list(options.keys()))
var_desc = options[var_key]

# סינון נתונים
df = data[['hospital_death', var_key]].dropna()
survived = df[df['hospital_death'] == 0][var_key]
died = df[df['hospital_death'] == 1][var_key]

# גרף
fig = go.Figure()
fig.add_trace(go.Histogram(x=survived, name='שורדים 🟢', marker_color='#00c853', opacity=0.75))
fig.add_trace(go.Histogram(x=died, name='נפטרים 🔴', marker_color='#ff5252', opacity=0.75))
fig.update_layout(barmode='overlay', title=f"{var_desc}", template='plotly_dark')

# מבחן t
t_stat, p_value = ttest_ind(survived, died, equal_var=False)
significant = '✅ כן' if p_value < 0.05 else '❌ לא'

# תוצאה טקסטואלית
st.plotly_chart(fig, use_container_width=True)
st.markdown(
    "#### 🧪 תוצאות סטטיסטיות:\n"
    f"- **ממוצע שורדים:** {survived.mean():.2f}  \n"
    f"- **ממוצע נפטרים:** {died.mean():.2f}  \n"
    f"- **P-Value:** {p_value:.4f}  \n"
    f"- **האם מובהק סטטיסטית:** {significant}"
)

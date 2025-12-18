import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Immersive Disaster Data Stories",
    layout="wide"
)

# --------------------------------
# TITLE & INTRO (NARRATIVE OPENING)
# --------------------------------
st.title("🌍 Immersive Visual Data Stories")
st.subheader("Global Disaster Response Analysis (2018–2024)")

st.markdown(
    """
    Visualisasi ini dirancang sebagai **cerita data visual imersif**
    untuk membantu memahami pola respons bencana global.
    Setiap bagian menyajikan satu narasi utama yang saling terhubung.
    """
)

# --------------------------------
# LOAD DATA
# --------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("global_disaster_response_2018_2024.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    return df

df = load_data()

# --------------------------------
# SIDEBAR – SIMPLE & CLEAN
# --------------------------------
st.sidebar.header("🔎 Filter Cerita Data")

year_range = st.sidebar.slider(
    "Rentang Tahun",
    int(df['year'].min()),
    int(df['year'].max()),
    (int(df['year'].min()), int(df['year'].max()))
)

selected_types = st.sidebar.multiselect(
    "Jenis Bencana",
    df['disaster_type'].unique(),
    default=df['disaster_type'].unique()
)

df_f = df[
    (df['year'] >= year_range[0]) &
    (df['year'] <= year_range[1]) &
    (df['disaster_type'].isin(selected_types))
]

# =====================================================
# STORY 1 — OVERVIEW
# =====================================================
st.markdown("## 🟦 Story 1: Pola Umum Bencana Global")

fig1 = px.bar(
    df_f,
    x="disaster_type",
    title="Distribusi Jenis Bencana",
    labels={"disaster_type": "Jenis Bencana"},
    color="disaster_type"
)

st.plotly_chart(fig1, use_container_width=True)

st.caption(
    "Visualisasi ini memperlihatkan jenis bencana yang paling sering terjadi, "
    "memberikan konteks awal sebelum analisis lebih mendalam."
)

# =====================================================
# STORY 2 — TEMPORAL FLOW
# =====================================================
st.markdown("## 🟧 Story 2: Dinamika Waktu Kejadian")

yearly = df_f.groupby("year").size().reset_index(name="count")

fig2 = px.line(
    yearly,
    x="year",
    y="count",
    markers=True,
    title="Tren Kejadian Bencana Global",
    labels={"year": "Tahun", "count": "Jumlah Kejadian"},
)

st.plotly_chart(fig2, use_container_width=True)

st.caption(
    "Alur temporal membantu pengguna memahami fluktuasi kejadian bencana "
    "dan perubahan pola dari tahun ke tahun."
)

# =====================================================
# STORY 3 — IMPACT & RESPONSE
# =====================================================
st.markdown("## 🔴 Story 3: Dampak dan Kecepatan Respons")

fig3 = px.scatter(
    df_f,
    x="response_time_hours",
    y="casualties",
    size="severity_index",
    color="disaster_type",
    title="Waktu Respons dan Dampak Korban",
    labels={
        "response_time_hours": "Waktu Respons (jam)",
        "casualties": "Jumlah Korban"
    }
)

st.plotly_chart(fig3, use_container_width=True)

st.caption(
    "Visualisasi ini menyoroti hubungan antara kecepatan respons "
    "dan tingkat dampak bencana."
)

# =====================================================
# STORY 4 — RECOVERY
# =====================================================
st.markdown("## 🟩 Story 4: Pemulihan Pascabencana")

fig4 = px.scatter(
    df_f,
    x="response_time_hours",
    y="recovery_days",
    color="severity_index",
    title="Respons dan Durasi Pemulihan",
    labels={
        "response_time_hours": "Waktu Respons (jam)",
        "recovery_days": "Durasi Pemulihan (hari)"
    },
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig4, use_container_width=True)

st.caption(
    "Cerita data diakhiri dengan analisis pemulihan, "
    "menghubungkan respons awal dengan dampak jangka panjang."
)

# --------------------------------
# DATA TRANSPARENCY
# --------------------------------
with st.expander("📄 Lihat Data"):
    st.dataframe(df_f.head(50))

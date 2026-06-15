import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Dashboard Ketahanan Pangan Jabar", layout="wide")

st.title("Analisis Harga Pangan & Pengaruh Cuaca Menjelang Idul Adha di Jawa Barat")
st.write("Dashboard interaktif ini dapat digunakan untuk menelusuri pengaruh cuaca dan pola musiman terhadap berbagai komoditas harga bahan pangan mulai dari tahun 2017 hingga pertengahan 2026.")

# 2. Load Data
@st.cache_data
def load_data():
    path = 'datasets/clean_dataset/clean_merged_dataset.csv' 
    data = pd.read_csv(path)
    data['Tanggal'] = pd.to_datetime(data['Tanggal'])
    
    # Mapping angka menjadi teks agar legend visualisasi mudah dibaca
    data['Fase_Waktu'] = data['Is_Idul_Adha_Week'].map({1: 'Minggu Idul Adha', 0: 'Hari Biasa'})
    return data

df = load_data()

# 3. Sidebar untuk Filter Interaktif
st.sidebar.header("Dashboard Harga Pangan Menjelang Idul Adha")
list_komoditas = df['Komoditas'].unique()
komoditas_terpilih = st.sidebar.selectbox("Pilih Komoditas Pangan:", list_komoditas)

# Filter dataset
df_filtered = df[df['Komoditas'] == komoditas_terpilih]

# ==========================================
# 4. IMPLEMENTASI LAYOUT DASHBOARD
# ==========================================

# --- BARIS 1: Tren Harga & Scatter Plot ---
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Tren Harga {komoditas_terpilih} Menjelang Hari H Idul Adha")
    
    # Menghapus color_discrete_sequence agar kembali warna-warni
    fig_line = px.line(df_filtered, 
                       x='Days_to_Idul_Adha', 
                       y='Harga', 
                       color='Tahun_Sumber',
                       labels={'Days_to_Idul_Adha': 'Hari Menuju Hari-H', 'Harga': 'Harga (Rp)'})
    
    fig_line.add_vline(x=0, line_width=2, line_dash="dash", line_color="#FF4B4B", annotation_text="Hari H")
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("Dampak Curah Hujan terhadap Harga")
    fig_scatter = px.scatter(df_filtered, 
                             x='PRECTOTCORR', 
                             y='Harga', 
                             color='Fase_Waktu',
                             labels={'PRECTOTCORR': 'Curah Hujan (mm/hari)', 'Harga': 'Harga (Rp)'},
                             # Kustomisasi warna titik: Hijau tua untuk minggu raya, Hijau muda untuk hari biasa
                             color_discrete_map={'Minggu Idul Adha': '#1E5631', 'Hari Biasa': '#A4D4B4'})
    
    st.plotly_chart(fig_scatter, use_container_width=True)


# --- BARIS 2: Distribusi & Korelasi ---
st.divider() # Garis pembatas
col3, col4 = st.columns(2)

with col3:
    st.subheader(f"Distribusi Harga: Hari Biasa vs Minggu Idul Adha")
    fig_box = px.box(df_filtered, 
                     x='Fase_Waktu', 
                     y='Harga', 
                     color='Fase_Waktu',
                     color_discrete_map={'Minggu Idul Adha': '#1E5631', 'Hari Biasa': '#A4D4B4'},
                     labels={'Fase_Waktu': 'Periode'})
    
    # Menghilangkan legend karena sumbu X sudah jelas
    fig_box.update_layout(showlegend=False) 
    st.plotly_chart(fig_box, use_container_width=True)

with col4:
    st.subheader(f"Korelasi Parameter Cuaca & Harga ({komoditas_terpilih})")
    # Memilih kolom numerik saja untuk heatmap
    cols_corr = ['Harga', 'T2M_MIN', 'T2M_MAX', 'T2M', 'RH2M', 'PRECTOTCORR', 'WS10M']
    df_corr = df_filtered[cols_corr].corr().round(2)
    
    fig_heat = px.imshow(df_corr, 
                         text_auto=True, 
                         aspect="auto",
                         # Menggunakan skala warna hijau-putih
                         color_continuous_scale='Greens')
    st.plotly_chart(fig_heat, use_container_width=True)

# ==========================================
# 5. FITUR FORECASTING (PREDIKSI HARGA)
# ==========================================
st.divider()
st.header(f"Prediksi Harga (Forecasting) - {komoditas_terpilih}")
st.write("Menggunakan Machine Learning (Random Forest) dengan pendekatan Rasio Kenaikan (memprediksi lonjakan dari Harga Baseline).")

# 1. Penyiapan Data Model (Mengikuti metode dari teman)
df_model = df_filtered.copy()
df_model = df_model.sort_values('Tanggal')

# Memastikan ada kolom 'Tahun'
df_model['Tahun'] = df_model['Tanggal'].dt.year

# Membuat fitur Harga Baseline dan Rasio Kenaikan
df_model['Harga_Baseline'] = df_model.groupby('Tahun')['Harga'].transform('first')
df_model['Rasio_Kenaikan'] = df_model['Harga'] / df_model['Harga_Baseline']

# Fitur prediktor murni cuaca dan waktu (tanpa Lag / MA)
features = ['Days_to_Idul_Adha', 'Is_Idul_Adha_Week', 'PRECTOTCORR', 'T2M', 'RH2M', 'WS10M']

# Pemisahan Data (Train < 2026, Test == 2026)
train_data = df_model[df_model['Tahun'] < 2026].copy()
test_data = df_model[df_model['Tahun'] == 2026].copy()

# Target Training adalah Rasio (Bukan Harga)
X_train = train_data[features]
y_train_ratio = train_data['Rasio_Kenaikan']

X_test = test_data[features]
y_test_harga_aktual = test_data['Harga']

# 2. Melatih Model via Cache
@st.cache_resource 
def train_rf_model(X, y):
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    return rf

# Model dilatih untuk memprediksi Rasio
model_rf = train_rf_model(X_train, y_train_ratio)

# 3. Melakukan Prediksi & Konversi kembali ke Harga Rupiah
test_data['Prediksi_Rasio'] = model_rf.predict(X_test)
test_data['Prediksi_Harga'] = test_data['Prediksi_Rasio'] * test_data['Harga_Baseline']

# Menghitung Metrik Error
mape = mean_absolute_percentage_error(y_test_harga_aktual, test_data['Prediksi_Harga']) * 100

# ====================================================================
# 4. VISUALISASI REPLIKA (MENGGUNAKAN MATPLOTLIB & SEABORN)
# ====================================================================
sns.set_theme(style="whitegrid", rc={"axes.edgecolor": "black"})
fig, ax = plt.subplots(figsize=(15, 7))

ax.plot(test_data['Tanggal'], test_data['Harga'], 
        label='Harga Aktual (2026)', color='#2ca02c', marker='o', linewidth=2.5, markersize=6)

ax.plot(test_data['Tanggal'], test_data['Prediksi_Harga'], 
        label='Prediksi RF (Pendekatan Rasio Kenaikan)', color='#d62728', linestyle='--', marker='s', linewidth=2.5, markersize=6)

tgl_idul_adha = test_data[test_data['Is_Idul_Adha_Week'] == 1]['Tanggal']
if not tgl_idul_adha.empty:
    ax.axvspan(tgl_idul_adha.min(), tgl_idul_adha.max(), color='#ff7f0e', alpha=0.15, label='Fase Minggu Idul Adha')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.set_title(f'Prediksi Harga dengan Model Rasio Peningkatan\nKomoditas: {komoditas_terpilih.strip()} (Error MAPE: {mape:.2f}%)', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Periode Observasi (Tahun 2026)', fontsize=12, fontweight='bold')
ax.set_ylabel('Harga (Rp)', fontsize=12, fontweight='bold')

ax.legend(loc='upper left', frameon=True, shadow=True, fontsize=11)
plt.tight_layout()

# Render di web Streamlit
st.pyplot(fig)

# 5. Menampilkan Ringkasan Data di Bagian Bawah
st.divider()
st.subheader("Sampel Data Terintegrasi")
st.dataframe(df_filtered.tail(10), use_container_width=True)
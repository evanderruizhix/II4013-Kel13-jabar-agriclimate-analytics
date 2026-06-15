# Tugas Besar II4013 Data Analytics

## AgriClimate Idul Adha
*Website* ini dikembangkan dalam rangka memenuhi Tugas Besar II4013 Data Analytics.
 
**Kelompok 13**

Anggota:
1. Wilson / 18223012
2. Stevan Einer Bonagabe / 18223028
3. Favian Rafi Laftiyanto / 18223036
4. Ahmad Evander Ruizhi Xavier / 18223064
5. Derick Amadeus Budiono / 18223090

### A. Deskripsi
AgriClimate Idul Adha adalah dashboard analitik interaktif yang dirancang untuk menelusuri tren dan memvisualisasikan pengaruh cuaca terhadap fluktuasi harga bahan pangan pokok di Jawa Barat, khususnya pada periode kritis menjelang Hari Raya Idul Adha (Tahun 2017-2026).

Proyek ini dibangun untuk memberikan wawasan kuantitatif (insight) mengenai pola pergerakan harga historis dan menguji hipotesis korelasi antara anomali cuaca (seperti curah hujan dan suhu) dengan lonjakan harga pangan. Selain visualisasi data historis (Exploratory Data Analysis), dashboard ini mengintegrasikan model peramalan (*forecasting*) berbasis *Machine Learning* untuk memprediksi rasio kenaikan harga komoditas berdasarkan pendekatan &*baseline* tahunan. Seluruh pipeline, mulai dari *data ingestion*, *preprocessing*, hingga pemodelan, terstruktur secara berurutan dan dapat ditelusuri.

### B. Fitur Utama
1. **Filter Komoditas Bahan Pangan**: Pengguna dapat menyeleksi komoditas pangan spesifik (misal: Cabai Merah Keriting, Daging Sapi, dll.) melalui dropdown sidebar, di mana seluruh grafik dan metrik akan diperbarui secara real-time.

2. ***Tracking* Tren Harga Tahunan**: Line chart interaktif yang memetakan pergerakan harga secara presisi dari H-30 hingga Hari-H Idul Adha, membandingkan tren antar tahun dalam satu kanvas.

3. **Analisis Pengaruh Cuaca**: Eksplorasi multivariat menggunakan Scatter Plot untuk melihat titik kumpul korelasi antara curah hujan, periode perayaan, dan harga, serta Heatmap dinamis untuk melihat koefisien korelasi spesifik antar parameter cuaca (T2M, PRECTOTCORR, RH2M, dll) dengan harga.

4. **Perbandingan Volatilitas Harga**: Visualisasi Boxplot yang menyoroti perbandingan distribusi dan variansi harga komoditas pada minggu perayaan Idul Adha versus hari biasa untuk mendeteksi outlier dan volatilitas.

5. ***Machine Learning Forecasting***: Modul prediksi harga masa depan menggunakan algoritma Random Forest Regressor. Model ini menggunakan pendekatan rasio peningkatan dari harga baseline awal tahun dan dilatih secara *on-the-fly* (*cache-optimized*) dengan evaluasi akurasi metrik MAPE (*Mean Absolute Percentage Error*).

### C. Technology Stack yang Digunakan
- Notebook: .ipynb
- Dataset: .csv, .xslx
- *Frontend & Dashboard*: Streamlit (Python *web-based app*).
- *Data Ingestion* & Pengolahan Data: Python, pandas, numpy, API (portal open data cuaca/NASA POWER).
- Visualisasi Data: plotly.express (untuk grafik interaktif), matplotlib, seaborn (untuk replika visualisasi statis presisi tinggi).
- *Machine Learning* & Analisis: scikit-learn (Algoritma Random Forest, Metrics Evaluation).

### D. Struktur Repositori
```
├── streamlit/
│ └── config.toml
├── datasets/
│ ├── raw_datasets/
│ │ ├── pihps_unmerged/
│ │ │ ├── Idul Adha 2017.xlsx
│ │ │ ├── Idul Adha 2018.xlsx
│ │ │ ├── Idul Adha 2019.xlsx
│ │ │ ├── Idul Adha 2020.xlsx
│ │ │ ├── Idul Adha 2021.xlsx
│ │ │ ├── Idul Adha 2022.xlsx
│ │ │ ├── Idul Adha 2023.xlsx
│ │ │ ├── Idul Adha 2024.xlsx
│ │ │ ├── Idul Adha 2025.xlsx
│ │ │ └── Idul Adha 2026.xlsx
│ │ ├── weather_nasa_untransformed/
│ │ │ └── POWER_Point_Daily_20170101_20260527_006d92S_107d61E_LST.csv
│ │ ├── all_price_iduladha_2017_2026.csv
│ │ └── all_weather_nasa_2017_2026.csv
│ └── clean_datasets/
│   └── clean_merged_datasets.csv
├── notebooks/
│ ├── 1_data_ingestion.ipynb
│ ├── 2_preprocessing.ipynb
│ ├── 3_eda.ipynb
│ └── 4_forecasting_model.ipynb
├── requirements.txt
├── app.py
└── README.md
```

### E. *Screenshot* Website
<img width="1837" height="816" alt="image" src="https://github.com/user-attachments/assets/f83dd84d-f5c6-4525-8abc-a32c9a219f13" />
<img width="1800" height="692" alt="image" src="https://github.com/user-attachments/assets/b1f5bceb-61aa-4d8c-912d-a5729491e3e9" />
<img width="1817" height="741" alt="image" src="https://github.com/user-attachments/assets/a624b2f3-691b-42f5-ad0e-17eca4deb7b8" />
<img width="1830" height="590" alt="image" src="https://github.com/user-attachments/assets/cd59833e-530c-48ce-a24d-b4c8a4e442ea" />

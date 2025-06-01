import numpy as np
import pandas as pd
import streamlit as st
import pickle

# Load model
model_prediksi = pickle.load(open("modelCB_terbaik.sav", "rb"))

# Custom CSS untuk latar belakang dan elemen UI
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #e0f7fa, #ffffff);
        }
        .stApp {
            background: linear-gradient(to right, #e0f7fa, #ffffff);
        }
        h1 {
            color: #0d47a1;
        }
        .stSelectbox label, .stNumberInput label {
            font-weight: bold;
            color: #0d47a1;
        }
        .stButton button {
            background-color: #0d47a1;
            color: white;
        }
        .stButton button:hover {
            background-color: #1565c0;
        }
    </style>
""", unsafe_allow_html=True)

# Judul
st.title("Prediksi Status Gizi Balita")
st.markdown("Silakan isi data berikut untuk mengetahui prediksi status gizi balita.")

# Kolom input (2 kolom)
col1, col2 = st.columns(2)

with col1:
    Jenis_Kelamin = st.selectbox("Pilih Jenis Kelamin", ["", "Laki-laki", "Perempuan"])
    Usia = st.number_input("Masukkan Usia (bulan)", min_value=0, step=1, format="%d")
    Berat_Badan_Lahir = st.number_input("Berat Badan Lahir (kg)", min_value=0.0, step=0.1, format="%.1f",
                                        help="Contoh: (2,5), (3,0), (3,2)")
    Tinggi_Badan_Lahir = st.number_input("Tinggi Badan Lahir (cm)", min_value=0.0, step=0.1, format="%.1f",
                                         help="Contoh: (48,0), (49,1), (50,0")
    Berat_Badan = st.number_input("Berat Badan Saat Ini (kg)", min_value=0.0, step=0.1, format="%.1f",
                                  help="Contoh: (8,0), (9,2), (10,5)")
    Tinggi_Badan = st.number_input("Tinggi Badan Saat Ini (cm)", min_value=0.0, step=0.1, format="%.1f",
                                   help="Contoh: (70,0), (72,5), (75,1)")
with col2:
    Status_Pemberian_ASI = st.selectbox("Status Pemberian ASI", ["", "Ya", "Tidak"])
    Status_Tinggi_Badan = st.selectbox("Kondisi Tinggi Badan Saat Ini", ["", "Sangat pendek", "Pendek", "Normal", "Tinggi"])
    Status_Berat_Badan = st.selectbox("Kondisi Berat Badan Saat Ini", ["", "Berat badan sangat kurang", "Berat badan kurang", "Berat badan normal", "Risiko berat badan lebih"])

# Mapping
jenis_kelamin_map = {'Laki-laki': 0, 'Perempuan': 1}
asi_map = {'Tidak': 0, 'Ya': 1}
berat_badan_map = {
    'Berat badan kurang': 0,
    'Berat badan normal': 1,
    'Berat badan sangat kurang': 2,
    'Risiko berat badan lebih': 3
}
tinggi_badan_map = {
    'Normal': 0,
    'Pendek': 1,
    'Sangat pendek': 2,
    'Tinggi': 3
}
status_gizi_map = {
    0: 'Berisiko gizi lebih',
    1: 'Gizi baik',
    2: 'Gizi buruk',
    3: 'Gizi kurang',
    4: 'Gizi lebih',
    5: 'Obesitas'
}

# Tombol Prediksi
if st.button("Tampilkan Hasil Prediksi"):
    if "" in (Jenis_Kelamin, Status_Pemberian_ASI, Status_Tinggi_Badan, Status_Berat_Badan):
        st.warning("Mohon lengkapi semua pilihan terlebih dahulu.")
    else:
        input_data = [[
            jenis_kelamin_map[Jenis_Kelamin],
            Usia,
            Berat_Badan_Lahir,
            Tinggi_Badan_Lahir,
            Berat_Badan,
            Tinggi_Badan,
            asi_map[Status_Pemberian_ASI],
            tinggi_badan_map[Status_Tinggi_Badan],
            berat_badan_map[Status_Berat_Badan]
        ]]

        hasil = model_prediksi.predict(input_data)
        gizi_diagnosis = status_gizi_map[int(hasil[0])]
        st.success(f"Hasil Prediksi Status Gizi Balita: **{gizi_diagnosis}**")

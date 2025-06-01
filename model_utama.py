import numpy as np
import pandas as pd
import streamlit as st
import pickle

# Fungsi load model berdasarkan pilihan algoritma
def load_model(algoritma):
    if algoritma == "CatBoost":
        return pickle.load(open("modelCB_terbaik.sav", "rb"))
    elif algoritma == "KNN":
        return pickle.load(open("modelKNN_terbaik.sav", "rb"))

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
        .stRadio label {
            font-weight: bold;
            color: #0d47a1;
        }
    </style>
""", unsafe_allow_html=True)

# Judul
st.title("Prediksi Status Gizi Balita Menggunakan Algoritma CatBoost dan KNN")
st.markdown("Lakukan pengisian data berikut untuk mengetahui prediksi status gizi balita.")

# Pilih algoritma dengan radio button
algoritma = st.radio("Pilih Algoritma yang akan digunakan:", ("CatBoost", "KNN"))

# Kolom input (2 kolom)
col1, col2 = st.columns(2)

with col1:
    Jenis_Kelamin = st.selectbox("Pilih Jenis Kelamin", ["", "Laki-laki", "Perempuan"])
    Usia = st.number_input("Masukkan Usia (bulan)", min_value=0, step=1, format="%d")
    Berat_Badan_Lahir = st.number_input("Berat Badan Lahir (kg)", min_value=0.0, step=0.1, format="%.1f",
                                        help="Contoh: 2,5")
    Tinggi_Badan_Lahir = st.number_input("Tinggi Badan Lahir (cm)", min_value=0.0, step=0.1, format="%.1f",
                                         help="Contoh: 48,0")
    Berat_Badan = st.number_input("Berat Badan Saat Ini (kg)", min_value=0.0, step=0.1, format="%.1f",
                                  help="Contoh: 10,5")
    Tinggi_Badan = st.number_input("Tinggi Badan Saat Ini (cm)", min_value=0.0, step=0.1, format="%.1f",
                                   help="Contoh: 70.0")
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

if st.button("Tampilkan Hasil Prediksi"):
    # Cek apakah ada input dropdown yang kosong
    if "" in (Jenis_Kelamin, Status_Pemberian_ASI, Status_Tinggi_Badan, Status_Berat_Badan):
        st.warning("Mohon lengkapi semua pilihan terlebih dahulu.")
    # Filter rentang usia
    elif not (1 <= Usia <= 59):
        st.warning("Usia harus antara 1 sampai 59 bulan.")
    # Filter rentang berat badan lahir
    elif not (1.8 <= Berat_Badan_Lahir <= 4.0):
        st.warning("Berat Badan Lahir harus antara 1.8 kg sampai 4.0 kg.")
    # Filter rentang tinggi badan lahir
    elif not (42.0 <= Tinggi_Badan_Lahir <= 53.0):
        st.warning("Tinggi Badan Lahir harus antara 42.0 cm sampai 53.0 cm.")
    # Filter rentang berat badan saat ini
    elif not (2.9 <= Berat_Badan <= 24.5):
        st.warning("Berat Badan Saat Ini harus antara 2.9 kg sampai 24.5 kg.")
    # Filter rentang tinggi badan saat ini
    elif not (49.0 <= Tinggi_Badan <= 111.0):
        st.warning("Tinggi Badan Saat Ini harus antara 49.0 cm sampai 111.0 cm.")
    else:
        # Load model sesuai pilihan algoritma
        model_prediksi = load_model(algoritma)
        
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
        st.success(f"Hasil Prediksi Status Gizi Balita menggunakan **{algoritma}**: **{gizi_diagnosis}**")

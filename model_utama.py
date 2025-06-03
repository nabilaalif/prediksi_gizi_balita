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

# Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #e3f2fd;
        }
        .stApp {
            background-color: #e3f2fd;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #0d47a1;
        }
        label, .css-1kyxreq, .css-1v0mbdj {
            font-weight: bold;
            color: #0d47a1;
        }
        button, .stButton > button {
            background-color: #0d47a1;
            color: white;
            border: none;
            padding: 0.4em 1.2em;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover, .stButton > button:hover {
            background-color: #1565c0;
        }
    </style>
""", unsafe_allow_html=True)

# Judul
st.markdown("<p style='font-size:22px; font-weight:bold; color:black;'>Prediksi Status Gizi Balita Menggunakan Algoritma CatBoost dan KNN</p>", unsafe_allow_html=True)

# Pilih algoritma
algoritma = st.radio("Pilih Algoritma yang akan digunakan:", ("CatBoost", "KNN"), key="algoritma")

st.markdown("Lakukan pengisian data berikut untuk mengetahui status gizi balita.")

# Input kolom
col1, col2 = st.columns(2)

with col1:
    jenis_kelamin = st.selectbox("Pilih Jenis Kelamin", ["Laki-laki", "Perempuan"])
    usia_input = st.text_input("Masukkan Usia (bulan)", placeholder="Contoh: 24")
    st.markdown("<div style='font-size:12px; color:gray;'>Masukkan nilai antara 1 hingga 59 bulan</div>", unsafe_allow_html=True)

    berat_lahir_input = st.text_input("Berat Badan Lahir (kg)", placeholder="Contoh: 3.2")
    st.markdown("<div style='font-size:12px; color:gray;'>Masukkan nilai antara 1.8 hingga 4.0 kg</div>", unsafe_allow_html=True)

    tinggi_lahir_input = st.text_input("Tinggi Badan Lahir (cm)", placeholder="Contoh: 50.0")
    st.markdown("<div style='font-size:12px; color:gray;'>Masukkan nilai antara 42.0 hingga 53.0 cm</div>", unsafe_allow_html=True)

    status_asi = st.selectbox("Status Pemberian ASI", ["Eksklusif", "Tidak Eksklusif"])

with col2:
    berat_input = st.text_input("Berat Badan Saat Ini (kg)", placeholder="Contoh: 12.5")
    st.markdown("<div style='font-size:12px; color:gray;'>Masukkan nilai antara 2.9 hingga 24.5 kg</div>", unsafe_allow_html=True)

    tinggi_input = st.text_input("Tinggi Badan Saat Ini (cm)", placeholder="Contoh: 75.0")
    st.markdown("<div style='font-size:12px; color:gray;'>Masukkan nilai antara 49.0 hingga 111.0 cm</div>", unsafe_allow_html=True)

    kondisi_tinggi = st.selectbox("Kondisi Tinggi Badan Saat Ini", ["Normal", "Pendek", "Sangat Pendek", "Tinggi"])
    kondisi_berat = st.selectbox("Kondisi Berat Badan Saat Ini", ["Berat badan normal", "Berat badan sangat kurang", "Berat badan kurang", "Risiko berat badan lebih"])

# Mapping
jenis_kelamin_map = {'Laki-laki': 0, 'Perempuan': 1}
asi_map = {'Tidak Eksklusif': 0, 'Eksklusif': 1}
berat_badan_map = {
    'Berat badan sangat kurang': 2,
    'Berat badan kurang': 0,
    'Berat badan normal': 1,
    'Risiko berat badan lebih': 3
}
tinggi_badan_map = {
    'Normal': 0,
    'Pendek': 1,
    'Sangat Pendek': 2,
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

# Validasi
def convert_and_validate_float(value, min_val, max_val, field_name):
    try:
        val = float(value.replace(',', '.'))
    except:
        st.error(f"Input {field_name} harus berupa angka.")
        return None
    if not min_val <= val <= max_val:
        st.warning(f"{field_name} harus dalam rentang {min_val} sampai {max_val}")
        return None
    return val

def convert_and_validate_int(value, min_val, max_val, field_name):
    try:
        val = int(value)
    except:
        st.error(f"{field_name} harus berupa bilangan bulat.")
        return None
    if not min_val <= val <= max_val:
        st.warning(f"{field_name} harus antara {min_val} sampai {max_val}")
        return None
    return val

# Tombol Prediksi
if st.button("Hasil Prediksi"):
    usia = convert_and_validate_int(usia_input, 1, 59, "Usia (bulan)")
    berat_lahir = convert_and_validate_float(berat_lahir_input, 1.8, 4.0, "Berat Badan Lahir (kg)")
    tinggi_lahir = convert_and_validate_float(tinggi_lahir_input, 42.0, 53.0, "Tinggi Badan Lahir (cm)")
    berat = convert_and_validate_float(berat_input, 2.9, 24.5, "Berat Badan Saat Ini (kg)")
    tinggi = convert_and_validate_float(tinggi_input, 49.0, 111.0, "Tinggi Badan Saat Ini (cm)")

    if None not in (usia, berat_lahir, tinggi_lahir, berat, tinggi):
        model = load_model(algoritma)

        fitur_input = [[
            jenis_kelamin_map[jenis_kelamin],
            usia,
            berat_lahir,
            tinggi_lahir,
            berat,
            tinggi,
            asi_map[status_asi],
            tinggi_badan_map[kondisi_tinggi],
            berat_badan_map[kondisi_berat]
        ]]

        hasil = model.predict(fitur_input)
        output = status_gizi_map.get(int(hasil[0]), "Tidak diketahui")

        st.success(f"Hasil Prediksi Status Gizi Balita dengan **{algoritma}** adalah: **{output}**")

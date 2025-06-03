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
col1, col2, col3 = st.columns(3)

with col1:
    jenis_kelamin = st.selectbox("Pilih Jenis Kelamin", ["Laki-laki", "Perempuan"])
    usia = st.text_input("Usia (bulan)", placeholder="Contoh: 24")
    st.markdown("<div style='font-size:14px; color:gray; margin-top: -10px; margin-bottom: 15px;'>Input nilai antara 1 hingga 59</div>", unsafe_allow_html=True)

    berat_lahir = st.text_input("Berat Badan Lahir (kg)", placeholder="Contoh: 3.2")
    st.markdown("<div style='font-size:14px; color:gray; margin-top: -10px; margin-bottom: 15px;'>Input nilai antara 1.8 hingga 4.0</div>", unsafe_allow_html=True)

with col2:
    tinggi_lahir = st.text_input("Tinggi Badan Lahir (cm)", placeholder="Contoh: 50.0")
    st.markdown("<div style='font-size:14px; color:gray; margin-top: -10px; margin-bottom: 15px;'>Input nilai antara 42.0 hingga 53.0</div>", unsafe_allow_html=True)

    berat_saat_ini = st.text_input("Berat Badan Saat Ini (kg)", placeholder="Contoh: 12.5")
    st.markdown("<div style='font-size:14px; color:gray; margin-top: -10px; margin-bottom: 15px;'>Input nilai antara 2.9 hingga 24.5</div>", unsafe_allow_html=True)

    tinggi_saat_ini = st.text_input("Tinggi Badan Saat Ini (cm)", placeholder="Contoh: 75.0")
    st.markdown("<div style='font-size:14px; color:gray; margin-top: -10px; margin-bottom: 15px;'>Input nilai antara 49.0 hingga 111.0</div>", unsafe_allow_html=True)

with col3:
    status_asi = st.selectbox("Status Pemberian ASI", ["Ya", "Tidak"])
    kondisi_tinggi = st.selectbox("Kondisi Tinggi Badan Saat Ini", ["Normal", "Pendek", "Sangat Pendek", "Tinggi"])
    kondisi_berat = st.selectbox("Kondisi Berat Badan Saat Ini", ["Berat badan normal", "Berat badan sangat kurang", "Berat badan kurang", "Risiko berat badan lebih"])

# Mapping data
jenis_kelamin_map = {'Laki-laki': 0, 'Perempuan': 1}
asi_map = {'Tidak': 0, 'Ya': 1}
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

# Fungsi validasi
def convert_and_validate_float(value, min_val, max_val, field_name):
    try:
        val = float(value.replace(',', '.'))
    except ValueError:
        st.markdown(f"<div style='padding: 0.5em; background-color: #f0f0f0;'>⚠️ Input untuk {field_name} harus berupa angka.</div>", unsafe_allow_html=True)
        return None
    if not (min_val <= val <= max_val):
        st.markdown(f"<div style='padding: 0.5em; background-color: #f0f0f0;'>⚠️ Input untuk {field_name} harus antara {min_val} sampai {max_val}.</div>", unsafe_allow_html=True)
        return None
    return val

def convert_and_validate_int(value, min_val, max_val, field_name):
    try:
        val = int(value)
    except ValueError:
        st.markdown(f"<div style='padding: 0.5em; background-color: #f0f0f0;'>⚠️ Input untuk {field_name} harus bilangan bulat.</div>", unsafe_allow_html=True)
        return None
    if not (min_val <= val <= max_val):
        st.markdown(f"<div style='padding: 0.5em; background-color: #f0f0f0;'>⚠️ Input untuk {field_name} harus antara {min_val} sampai {max_val}.</div>", unsafe_allow_html=True)
        return None
    return val

# Tombol Prediksi
if st.button("Hasil Prediksi"):
    usia_val = convert_and_validate_int(usia, 1, 59, "Usia (bulan)")
    bb_lahir_val = convert_and_validate_float(berat_lahir, 1.8, 4.0, "Berat Badan Lahir (kg)")
    tb_lahir_val = convert_and_validate_float(tinggi_lahir, 42.0, 53.0, "Tinggi Badan Lahir (cm)")
    bb_now_val = convert_and_validate_float(berat_saat_ini, 2.9, 24.5, "Berat Badan Saat Ini (kg)")
    tb_now_val = convert_and_validate_float(tinggi_saat_ini, 49.0, 111.0, "Tinggi Badan Saat Ini (cm)")

    if None not in (usia_val, bb_lahir_val, tb_lahir_val, bb_now_val, tb_now_val):
        model_prediksi = load_model(algoritma)
        input_data = [[
            jenis_kelamin_map[jenis_kelamin],
            usia_val,
            bb_lahir_val,
            tb_lahir_val,
            bb_now_val,
            tb_now_val,
            asi_map[status_asi],
            tinggi_badan_map[kondisi_tinggi],
            berat_badan_map[kondisi_berat]
        ]]
        hasil = model_prediksi.predict(input_data)
        gizi_diagnosis = status_gizi_map.get(int(hasil[0]), "Status gizi tidak diketahui")

        st.markdown(f"<p style='font-size:18px; font-weight:bold;'>Hasil Prediksi Status Gizi menggunakan <u>{algoritma}</u>: <span style='color:#0d47a1;'>{gizi_diagnosis}</span></p>", unsafe_allow_html=True)

# Tombol Clear Form
def clear_inputs():
    st.experimental_rerun()

st.button("Kosongkan Form untuk Mengisi Kembali", on_click=clear_inputs)

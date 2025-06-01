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
st.header("Prediksi Status Gizi Balita Menggunakan Algoritma CatBoost dan KNN")
st.markdown("Lakukan pengisian data berikut untuk mengetahui status gizi balita.")

# Pilih algoritma dengan radio button
algoritma = st.radio("Pilih Algoritma yang akan digunakan:", ("CatBoost", "KNN"), key="algoritma")

# Inisialisasi session state default jika belum ada
default_values = {
    "Jenis_Kelamin": "",
    "Usia_input": "",
    "Berat_Badan_Lahir_input": "",
    "Tinggi_Badan_Lahir_input": "",
    "Berat_Badan_input": "",
    "Tinggi_Badan_input": "",
    "Status_Pemberian_ASI": "",
    "Status_Tinggi_Badan": "",
    "Status_Berat_Badan": ""
}

for key in default_values:
    if key not in st.session_state:
        st.session_state[key] = default_values[key]

# Kolom input (3 kolom)
col1, col2, col3 = st.columns(3)

with col1:
    Jenis_Kelamin = st.selectbox("Pilih Jenis Kelamin", ["", "Laki-laki", "Perempuan"], key="Jenis_Kelamin")
    Usia_input = st.text_input("Masukkan Usia (bulan)", placeholder="Contoh: 24", key="Usia_input")
    Berat_Badan_Lahir_input = st.text_input("Berat Badan Lahir (kg)", placeholder="Contoh: 3.2", key="Berat_Badan_Lahir_input")

with col2:
    Tinggi_Badan_Lahir_input = st.text_input("Tinggi Badan Lahir (cm)", placeholder="Contoh: 50.0", key="Tinggi_Badan_Lahir_input")
    Berat_Badan_input = st.text_input("Berat Badan Saat Ini (kg)", placeholder="Contoh: 12.5", key="Berat_Badan_input")
    Tinggi_Badan_input = st.text_input("Tinggi Badan Saat Ini (cm)", placeholder="Contoh: 75.0", key="Tinggi_Badan_input")

with col3:
    Status_Pemberian_ASI = st.selectbox("Status Pemberian ASI", ["", "Ya", "Tidak"], key="Status_Pemberian_ASI")
    Status_Tinggi_Badan = st.selectbox("Kondisi Tinggi Badan Saat Ini", ["", "Sangat pendek", "Pendek", "Normal", "Tinggi"], key="Status_Tinggi_Badan")
    Status_Berat_Badan = st.selectbox("Kondisi Berat Badan Saat Ini", ["", "Berat badan sangat kurang", "Berat badan kurang", "Berat badan normal", "Risiko berat badan lebih"], key="Status_Berat_Badan")

# Mapping tetap sama
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

def convert_and_validate_float(value, min_val, max_val, field_name):
    try:
        val = float(value.replace(',', '.'))  # Mengatasi input desimal dengan koma
    except ValueError:
        st.warning(f"Input untuk {field_name} harus berupa angka yang valid.")
        return None
    if not (min_val <= val <= max_val):
        st.warning(f"Input untuk {field_name} harus antara {min_val} sampai {max_val}.")
        return None
    return val

def convert_and_validate_int(value, min_val, max_val, field_name):
    try:
        val = int(value)
    except ValueError:
        st.warning(f"Input untuk {field_name} harus berupa angka bulat yang valid.")
        return None
    if not (min_val <= val <= max_val):
        st.warning(f"Input untuk {field_name} harus antara {min_val} sampai {max_val}.")
        return None
    return val

# Tombol Tampilkan Hasil Prediksi di bawah form input
if st.button("Hasil Prediksi"):
    # Cek dulu dropdown apakah ada yang belum dipilih
    if "" in (Jenis_Kelamin, Status_Pemberian_ASI, Status_Tinggi_Badan, Status_Berat_Badan):
        st.warning("Mohon lengkapi semua pilihan terlebih dahulu.")
    else:
        # Validasi input numerik
        Usia = convert_and_validate_int(Usia_input, 1, 59, "Usia (bulan)")
        Berat_Badan_Lahir = convert_and_validate_float(Berat_Badan_Lahir_input, 1.8, 4.0, "Berat Badan Lahir (kg)")
        Tinggi_Badan_Lahir = convert_and_validate_float(Tinggi_Badan_Lahir_input, 42.0, 53.0, "Tinggi Badan Lahir (cm)")
        Berat_Badan = convert_and_validate_float(Berat_Badan_input, 2.9, 24.5, "Berat Badan Saat Ini (kg)")
        Tinggi_Badan = convert_and_validate_float(Tinggi_Badan_input, 49.0, 111.0, "Tinggi Badan Saat Ini (cm)")

        # Jika semua validasi berhasil (tidak None)
        if None not in (Usia, Berat_Badan_Lahir, Tinggi_Badan_Lahir, Berat_Badan, Tinggi_Badan):
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
            gizi_diagnosis = status_gizi_map.get(int(hasil[0]), "Status gizi tidak diketahui")
            st.success(f"Hasil Prediksi Status Gizi Balita menggunakan **{algoritma}**: **{gizi_diagnosis}**")

# Tombol Clear muncul **setelah** tombol prediksi
def clear_inputs():
    for key in default_values:
        st.session_state[key] = default_values[key]

st.button("Kosongkan Form untuk Mengisi Kembali", on_click=clear_inputs)

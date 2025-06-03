if st.button("Hasil Prediksi"):
    if "" in (Jenis_Kelamin, Status_Pemberian_ASI, Status_Tinggi_Badan, Status_Berat_Badan):
        st.warning("Mohon lengkapi semua pilihan terlebih dahulu.")
    else:
        Usia = convert_and_validate_int(Usia_input, 1, 59, "Usia (bulan)")
        Berat_Badan_Lahir = convert_and_validate_float(Berat_Badan_Lahir_input, 1.8, 4.0, "Berat Badan Lahir (kg)")
        Tinggi_Badan_Lahir = convert_and_validate_float(Tinggi_Badan_Lahir_input, 42.0, 53.0, "Tinggi Badan Lahir (cm)")
        Berat_Badan = convert_and_validate_float(Berat_Badan_input, 2.9, 24.5, "Berat Badan Saat Ini (kg)")
        Tinggi_Badan = convert_and_validate_float(Tinggi_Badan_input, 49.0, 111.0, "Tinggi Badan Saat Ini (cm)")

        if None not in (Usia, Berat_Badan_Lahir, Tinggi_Badan_Lahir, Berat_Badan, Tinggi_Badan):
            model_prediksi = load_model(algoritma)
            if model_prediksi is not None:
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
                st.markdown(f"<p style='font-size:18px; font-weight:bold; color:black;'>Hasil Prediksi Status Gizi Balita menggunakan {algoritma}: <span style='color:#0d47a1;'>{gizi_diagnosis}</span></p>", unsafe_allow_html=True)

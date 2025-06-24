import streamlit as st
import pickle
import numpy as np
import pandas as pd
from PIL import Image

# Load model dan data
pipe = pickle.load(open('pipe_mobkas.pkl', 'rb'))
df = pickle.load(open('df_mobkas.pkl', 'rb'))

# Konfigurasi halaman
st.set_page_config(page_title="Prediksi Harga Audi Bekas Secara Akurat & Instan", layout="wide")

# ===== Hero Section =====
st.markdown("## ")
col1, col2 = st.columns([2, 1])  # Kolom teks lebih lebar dari kolom gambar

with col1:
    st.markdown("""
        <div style='padding: 20px 10px 20px 0px;'>
            <h1 style='font-size: 40px; color: #003366; margin-bottom: 10px;'>Prediksi Harga Mobil Audi Bekas<br>Secara Akurat & Instan</h1>
            <p style='font-size: 10px; color: #444;'>Powered by Machine Learning</p>
            <p style='font-size: 14px;'> <a href="#form-input"><u>Klik di sini untuk mulai prediksi</u></a></p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    try:
        img = Image.open("33.png")
        st.image(img, use_container_width=True)  
        
    except:
        st.warning("⚠️ Gambar tidak ditemukan. Pastikan file '15.png' berada di folder yang sama dengan file .py Anda.")

# ===== Deskripsi Audi =====
st.markdown("---")
deskripsi = """
Audi adalah produsen otomotif premium asal Jerman yang dikenal dengan perpaduan desain elegan, teknologi mutakhir, dan performa tinggi. Sebagai bagian dari Volkswagen Group, Audi konsisten menghadirkan inovasi melalui filosofi “Vorsprung durch Technik” keunggulan melalui teknologi yang menjadi ciri khas setiap modelnya.
Mulai dari city car yang cocok untuk jalanan kota Jakarta, hingga supercar berperforma ekstrem, Audi menawarkan kenyamanan dan kendali dalam balutan kemewahan khas Eropa. Fitur-fitur seperti sistem infotainment MMI, lampu matrix LED, dan teknologi bantuan berkendara semakin relevan dengan gaya hidup modern masyarakat urban di Indonesia.
Di pasar mobil bekas Indonesia, Audi menjadi simbol prestise yang semakin terjangkau. Banyak konsumen cerdas kini melirik Audi bekas sebagai alternatif kendaraan mewah dengan harga kompetitif. Dengan pilihan model yang beragam dan kualitas teknik Jerman yang terbukti, mobil Audi bekas tetap menawarkan nilai investasi tinggi, terutama bila dirawat dengan baik. Cocok untuk mereka yang ingin tampil elegan dan berbeda, tanpa harus membeli mobil baru.
"""
st.markdown(f"<div style='text-align: justify;'>{deskripsi}</div>", unsafe_allow_html=True)

# ===== Form Input =====
st.markdown("---")
st.markdown('<h2 id="form-input">Masukkan Detail Mobil Anda</h2>', unsafe_allow_html=True)

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        model = st.selectbox('Model Mobil', df['model'].unique())
        year = st.selectbox('Tahun Mobil', sorted(df['year'].unique(), reverse=True))
        transmission = st.selectbox('Transmisi', df['transmission'].unique())
        fuelType = st.selectbox('Jenis Bahan Bakar', df['fuelType'].unique())

    with col2:
        mileage = st.number_input('Jarak Tempuh (dalam mil)', min_value=0)
        tax = st.number_input('Pajak (dalam £)', min_value=0)
        mpg = st.number_input('Konsumsi Bahan Bakar (mpg)', min_value=0.0)
        engineSize = st.number_input('Ukuran Mesin (Liter)', min_value=0.0)

    submitted = st.form_submit_button("🔍 Prediksi Harga")

    if submitted:
        query = pd.DataFrame({
            'model': [model],
            'year': [year],
            'transmission': [transmission],
            'fuelType': [fuelType],
            'mileage': [mileage],
            'tax': [tax],
            'mpg': [mpg],
            'engineSize': [engineSize]
        })

        prediction = int(np.exp(pipe.predict(query)[0]) * 20000)

        st.success("✅ Prediksi Berhasil!")
        st.markdown(f"""
            <div style='background-color: #e6f2ff; padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: #004aad;'>Estimasi Harga Mobil Audi Bekas Anda</h3>
                <p style='font-size: 30px; font-weight: bold; color: #007BFF;'>Rp {prediction:,}</p>
            </div>
        """, unsafe_allow_html=True)

# ===== Footer =====
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>© 2025 Audi Price Predictor | Powered by Streamlit</p>", unsafe_allow_html=True)

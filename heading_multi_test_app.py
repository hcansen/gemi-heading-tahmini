import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import os

st.markdown("<h1 style='color:#0e1117;'>⛵︎ Gemi Manevra Testi Simülasyonu</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Kullanıcının seçeceği test türleri ve modelleri
test_models = {
    "Zigzag 10°": "zigzag_10_model_cloud13.pkl",
    "35° Sancak Dönüşü": "sancak_35_model_cloud13.pkl",
    "35° İskele Dönüşü": "iskele_35_model_cloud13.pkl"
}

}
}

}

# Test türünü seçtir
selected_test = st.selectbox("◉ Test Türünü Seçin", list(test_models.keys()))
model_file = test_models[selected_test]

# Modeli yükle
model_path = os.path.abspath(model_file)
model = joblib.load(model_path)

# CSV yükle
st.markdown("### 📥 CSV Dosyası Yükleyin")
uploaded_file = st.file_uploader("Rudder ve speed_total içeren bir dosya yükleyin", type=["csv"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        if 'rudder' in data.columns and 'speed_total' in data.columns:
            X_input = data[['rudder', 'speed_total']].astype(float)
            y_pred = model.predict(X_input) % 360
            data['Predicted_Heading'] = y_pred

            st.markdown("### 📋 Tahmin Sonuçları")
            st.dataframe(data)

            st.markdown("### 📈 Test Simülasyonu Grafiği")
            fig, ax = plt.subplots()
            ax.plot(data['Predicted_Heading'], marker='o', linestyle='-', color='darkorange')
            ax.set_title(f"{selected_test} - Heading Tahmini")
            ax.set_ylabel("Heading (°)")
            ax.set_xlabel("Zaman / Girdi Sırası")
            ax.set_ylim(0, 360)
            st.pyplot(fig)

            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("📤 Sonuçları CSV olarak indir", data=csv, file_name="tahmin_sonuclari.csv")

        else:
            st.error("❌ 'rudder' ve 'speed_total' sütunları bulunamadı.")
    except Exception as e:
        st.error(f"⚠️ Hata: {str(e)}")

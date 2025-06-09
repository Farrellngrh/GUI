import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Statistika Deskriptif", layout="wide")
st.markdown("<h1 style='text-align: center;'>Analisis Statistika Deskriptif</h1>", unsafe_allow_html=True)
st.divider()

st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Unggah file CSV atau Excel", type=["csv", "xls", "xlsx"])

with st.sidebar.expander("Apa itu Statistika Deskriptif?"):
    st.markdown("""
    **Statistika Deskriptif** digunakan untuk menyajikan, meringkas, dan menggambarkan data. 
    Analisis ini memberikan wawasan awal sebelum analisis lanjutan.

    Fitur:
    - Ringkasan statistik (mean, median, dll)
    - Struktur data (tipe variabel)
    - Korelasi antar variabel numerik
    - Distribusi data
    - Visualisasi Boxplot
    """)

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset")
    st.dataframe(df, use_container_width=True)

    st.markdown("### Struktur Data")
    structure_df = pd.DataFrame({
        "Kolom": df.columns,
        "Tipe Data": df.dtypes.values,
        "Jumlah Null": df.isnull().sum().values,
        "Jumlah Unik": df.nunique().values
    })
    st.dataframe(structure_df)

    st.markdown("### Ringkasan Statistik")
    st.dataframe(df.describe().T)

    # Korelasi
    st.markdown("### Korelasi antar Variabel Numerik")
    num_df = df.select_dtypes(include=np.number)
    if not num_df.empty:
        corr = num_df.corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Tidak ada kolom numerik untuk analisis korelasi.")

    # Distribusi Histogram
    st.markdown("### Distribusi Data (Histogram)")
    for col in num_df.columns:
        st.markdown(f"#### {col}")
        fig, ax = plt.subplots()
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        st.pyplot(fig)

    # Boxplot
    st.markdown("### Visualisasi Boxplot")
    for col in num_df.columns:
        st.markdown(f"#### {col}")
        fig, ax = plt.subplots()
        sns.boxplot(y=df[col], ax=ax)
        st.pyplot(fig)

else:
    st.info("Silakan unggah file CSV atau Excel melalui sidebar.")

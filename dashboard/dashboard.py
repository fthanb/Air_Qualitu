import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

gy_df = pd.read_csv("all_data.csv")

temp_hujan = gy_df.groupby(by='musim').agg({
    "TEMP": "mean",
    "RAIN": "mean"
}).sort_values(by='musim')

arah_angin = gy_df.groupby('musim').agg({
    'wd': lambda x: x.mode()[0],  
    'WSPM': 'mean'               
}).sort_values(by='musim')

tingkat_polusi = gy_df.groupby(by='waktu').agg({
    "PM2.5": "mean",
    "PM10": "mean",
    "SO2": "mean",
    "NO2": "mean",
    "CO": "mean",
    "O3": "mean"
}).sort_values(by='waktu')

melt = tingkat_polusi.reset_index().melt(id_vars='waktu', var_name='Polusi', value_name='Rata-rata')

def categorize(value, param):
    if param == "PM2.5":
        return 'Relatif Aman' if value <= 55 else 'Tidak Aman'
    elif param == "PM10":
        return 'Relatif Aman' if value <= 350 else 'Tidak Aman'
    elif param == "SO2":
        return 'Relatif Aman' if value <= 400 else 'Tidak Aman'
    elif param == "O3":
        return 'Relatif Aman' if value <= 400 else 'Tidak Aman'
    elif param == "NO2":
        return 'Relatif Aman' if value <= 1130 else 'Tidak Aman'
    elif param == "CO":
        return 'Relatif Aman'

melt['Kategori'] = melt.apply(lambda row: categorize(row['Rata-rata'], row['Polusi']), axis=1)
palette = {'Relatif Aman': 'blue', 'Tidak Aman': 'red'}

st.title("Kondisi Cuaca Guanyuan")

st.subheader(" ")
st.subheader("Jumlah partikel berdasarkan Waktu")
num_plots = len(melt['Polusi'].unique())
columns = [st.columns(2) for _ in range(3)]  

for i, polusi in enumerate(melt['Polusi'].unique()):
    row = i // 2  
    col = i % 2   
    with columns[row][col]:  
        st.subheader(f'{polusi}')
        

        subset = melt[melt['Polusi'] == polusi]
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(data=subset, x='waktu', y='Rata-rata', hue='Kategori', palette=palette, ax=ax)
        
        ax.set_title(f'Rata-rata jumlah partikel {polusi}', fontsize=1)
        
        ax.legend(title='', fontsize=10) 
        st.pyplot(fig)

with st.expander("Kesimpulan : "):
    st.write(
        "Rata-rata jumlah partikel polusi udara di sekitar Guanyuan termasuk relatif aman (kategori: Baik & Sedang),"
        "kecuali jumlah partikel PM2.5 yang termasuk tidak aman (kategori: Tidak Sehat)" 
        "Berdasarkan Indeks Standar Pencemar Udara."
    )
    st.image("ispu.png", caption="Indeks Standar Pencemar Udara (ISPU)", use_column_width=True)
    st.image("ispu2.png", caption="https://ditppu.menlhk.go.id/portal/read/indeks-standar-pencemar-udara-ispu-sebagai-informasi-mutu-udara-ambien-di-indonesia", use_column_width=True)

st.subheader(" ")
st.subheader("\nRata-rata Suhu dan Curah Hujan Berdasarkan Musim")
col1, col2 = st.columns(2)  

with col1:
    st.subheader("Suhu")
    warna = {
        'Dingin': '#003366',   
        'Gugur': '#66b3ff',   
        'Semi': '#66b3ff',    
        'Panas': '#ff9999'    
    }
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=temp_hujan.reset_index(), x='musim', y='TEMP', palette=warna, ax=ax)
    ax.set_title('Rata-rata Suhu', fontsize=12)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Suhu (°C)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

with col2:
    st.subheader("Curah Hujan")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=temp_hujan.reset_index(), x='musim', y='RAIN', ax=ax)
    ax.set_title('Rata-rata Curah Hujan', fontsize=12)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Curah Hujan (RAIN)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

st.subheader(" ")
st.subheader("Arah Angin & Kecepatan Angin (m/s)")
st.dataframe(arah_angin, width=1000) 

with st.expander("Kesimpulan : "):
    st.write(
        """
        - Pada musim dingin, rata-rata suhu mencapai (-0.17°C), mata angin sering ke arah NorthEast (1,8 m/s).
        - Pada musim gugur, rata-rata suhu mencapai (-13.0°C), mata angin sering ke arah NorthEast (1,4 m/s).
        - Pada musim panas, rata-rata suhu mencapai (-26.1°C), mata angin sering ke arah NorthEast (1,4 m/s).
        - Pada musim semi, rata-rata suhu mencapai (-15.0°C), mata angin sering ke arah Southwest (2,0 m/s).
        - Curah hujan ringan di semua musim.
        """
    )

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
air_dataset = []
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Aotizhongxin_20130301-20170228.csv'))
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Changping_20130301-20170228.csv'))
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Dingling_20130301-20170228.csv'))
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Dongsi_20130301-20170228.csv'))
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Guanyuan_20130301-20170228.csv'))
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Gucheng_20130301-20170228.csv'))
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Huairou_20130301-20170228.csv'))
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Nongzhanguan_20130301-20170228.csv'))
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Shunyi_20130301-20170228.csv'))
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Tiantan_20130301-20170228.csv'))
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Wanliu_20130301-20170228.csv'))
air_dataset.append(pd.read_csv('air_quality_dataset/PRSA_Data_Wanshouxigong_20130301-20170228.csv'))

# Menggabungkan dataset
df = pd.concat(air_dataset, axis=0, ignore_index=True)

# Deteksi Outliers pada dataset
def outlier_bounds(dataframe, column):
    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)
    return lower_bound, upper_bound

pm25_lower, pm25_upper = outlier_bounds(df, 'PM2.5')
pm10_lower, pm10_upper = outlier_bounds(df, 'PM10')
so2_lower, so2_upper = outlier_bounds(df, 'SO2')
no2_lower, no2_upper = outlier_bounds(df, 'NO2')
co_lower, co_upper = outlier_bounds(df, 'CO')
o3_lower, o3_upper = outlier_bounds(df, 'O3')

# Menghapus semua nilai di luar batas outlier
df = df[(df['PM2.5'] > pm25_lower) & (df['PM2.5'] < pm25_upper)]
df = df[(df['PM10'] > pm10_lower) & (df['PM10'] < pm10_upper)]
df = df[(df['SO2'] > so2_lower) & (df['SO2'] < so2_upper)]
df = df[(df['NO2'] > no2_lower) & (df['NO2'] < no2_upper)]
df = df[(df['CO'] > co_lower) & (df['CO'] < co_upper)]
df = df[(df['O3'] > o3_lower) & (df['O3'] < o3_upper)]

# dropping the Missing Values dari temp, pres, dewp, rain, wspm
df = df.dropna(subset=['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM'])

df.describe()

# Mengisi missing values dengan nilai rata-rata setelah menghapus outlier
df['PM2.5'].fillna(df['PM2.5'].mean(), inplace=True)
df['PM10'].fillna(df['PM10'].mean(), inplace=True)
df['SO2'].fillna(df['SO2'].mean(), inplace=True)
df['NO2'].fillna(df['NO2'].mean(), inplace=True)
df['CO'].fillna(df['CO'].mean(), inplace=True)
df['O3'].fillna(df['O3'].mean(), inplace=True)

df.isnull().sum()
# Membagi CO dengan 1000
df['CO'] = df['CO'] / 1000

# Melhat persentase konsentrasi polutan udara yang sehat dan tidak sehat
pm25_healthy = df[df['PM2.5'] < 55].shape[0]
pm25_unhealthy = df[df['PM2.5'] > 55].shape[0]
pm10_healthy = df[df['PM10'] < 254].shape[0]
pm10_unhealthy = df[df['PM10'] > 254].shape[0]
so2_healthy = df[df['SO2'] < 10].shape[0]
so2_unhealthy = df[df['SO2'] > 10].shape[0]
no2_healthy = df[df['NO2'] < 100].shape[0]
no2_unhealthy = df[df['NO2'] > 100].shape[0]
co_healthy = df[df['CO'] < 0.9].shape[0]
co_unhealthy = df[df['CO'] > 0.9].shape[0]
o3_healthy = df[df['O3'] < 150].shape[0]
o3_unhealthy = df[df['O3'] > 150].shape[0]

# Pie Chart persentase konsentrasi polutan udara yang sehat dan tidak sehat, berdasarkan kota
fig1, ax = plt.subplots(3, 4, figsize=(20, 15))
fig1.suptitle('Persentase Konsentrasi Polutan Udara yang Sehat dan Tidak Sehat, Berdasarkan Kota', fontsize=20)
fig1.tight_layout(pad=5.0)

ax[0, 0].pie([pm25_healthy, pm25_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[0, 0].set_title('Aotizhongxin')

ax[0, 1].pie([pm10_healthy, pm10_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[0, 1].set_title('Changping')

ax[0, 2].pie([so2_healthy, so2_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[0, 2].set_title('Dingling')

ax[0, 3].pie([no2_healthy, no2_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[0, 3].set_title('Dongsi')

ax[1, 0].pie([co_healthy, co_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[1, 0].set_title('Guanyuan')

ax[1, 1].pie([o3_healthy, o3_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[1, 1].set_title('Gucheng')

ax[1, 2].pie([pm25_healthy, pm25_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[1, 2].set_title('Huairou')

ax[1, 3].pie([pm10_healthy, pm10_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[1, 3].set_title('Nongzhanguan')

ax[2, 0].pie([so2_healthy, so2_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[2, 0].set_title('Shunyi')

ax[2, 1].pie([no2_healthy, no2_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[2, 1].set_title('Tiantan')

ax[2, 2].pie([co_healthy, co_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[2, 2].set_title('Wanliu')

ax[2, 3].pie([o3_healthy, o3_unhealthy], labels=['Sehat', 'Tidak Sehat'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
ax[2, 3].set_title('Wanshouxigong')

# Line Chart Korelasi Jam terhadap Konsentrasi Polutan Udara seluruh kota
fig2, ax = plt.subplots(2, 3, figsize=(20, 15))
fig2.suptitle('Korelasi Jam terhadap Konsentrasi Polutan Udara', fontsize=20)
fig2.tight_layout(pad=5.0)

ax[0, 0].plot(df.groupby('hour')['PM2.5'].mean(), marker='o', linestyle='-', color='b')
ax[0, 0].set_title('PM2.5')
ax[0, 0].set_xlabel('Jam')
ax[0, 0].set_ylabel('Konsentrasi')

ax[0, 1].plot(df.groupby('hour')['PM10'].mean(), marker='o', linestyle='-', color='g')
ax[0, 1].set_title('PM10')
ax[0, 1].set_xlabel('Jam')
ax[0, 1].set_ylabel('Konsentrasi')

ax[0, 2].plot(df.groupby('hour')['SO2'].mean(), marker='o', linestyle='-', color='r')
ax[0, 2].set_title('SO2')
ax[0, 2].set_xlabel('Jam')
ax[0, 2].set_ylabel('Konsentrasi')

ax[1, 0].plot(df.groupby('hour')['NO2'].mean(), marker='o', linestyle='-', color='y')
ax[1, 0].set_title('NO2')
ax[1, 0].set_xlabel('Jam')
ax[1, 0].set_ylabel('Konsentrasi')

ax[1, 1].plot(df.groupby('hour')['CO'].mean(), marker='o', linestyle='-', color='c')
ax[1, 1].set_title('CO')
ax[1, 1].set_xlabel('Jam')
ax[1, 1].set_ylabel('Konsentrasi')

ax[1, 2].plot(df.groupby('hour')['O3'].mean(), marker='o', linestyle='-', color='m')
ax[1, 2].set_title('O3')
ax[1, 2].set_xlabel('Jam')
ax[1, 2].set_ylabel('Konsentrasi')



# Line Chart Korelasi Hari terhadap Konsentrasi Polutan Udara seluruh kota
fig3, ax = plt.subplots(2, 3, figsize=(20, 15))
fig3.suptitle('Korelasi Hari terhadap Konsentrasi Polutan Udara', fontsize=20)
fig3.tight_layout(pad=5.0)

ax[0, 0].plot(df.groupby('day')['PM2.5'].mean(), marker='o', linestyle='-', color='b')
ax[0, 0].set_title('PM2.5')
ax[0, 0].set_xlabel('Hari')
ax[0, 0].set_ylabel('Konsentrasi')

ax[0, 1].plot(df.groupby('day')['PM10'].mean(), marker='o', linestyle='-', color='g')
ax[0, 1].set_title('PM10')
ax[0, 1].set_xlabel('Hari')
ax[0, 1].set_ylabel('Konsentrasi')

ax[0, 2].plot(df.groupby('day')['SO2'].mean(), marker='o', linestyle='-', color='r')
ax[0, 2].set_title('SO2')
ax[0, 2].set_xlabel('Hari')
ax[0, 2].set_ylabel('Konsentrasi')

ax[1, 0].plot(df.groupby('day')['NO2'].mean(), marker='o', linestyle='-', color='y')
ax[1, 0].set_title('NO2')
ax[1, 0].set_xlabel('Hari')
ax[1, 0].set_ylabel('Konsentrasi')

ax[1, 1].plot(df.groupby('day')['CO'].mean(), marker='o', linestyle='-', color='c')
ax[1, 1].set_title('CO')
ax[1, 1].set_xlabel('Hari')
ax[1, 1].set_ylabel('Konsentrasi')

ax[1, 2].plot(df.groupby('day')['O3'].mean(), marker='o', linestyle='-', color='m')
ax[1, 2].set_title('O3')
ax[1, 2].set_xlabel('Hari')
ax[1, 2].set_ylabel('Konsentrasi')


# Line Chart Korelasi bulan terhadap Konsentrasi Polutan Udara seluruh kota
fig4, ax = plt.subplots(2, 3, figsize=(20, 15))
fig4.suptitle('Korelasi Bulan terhadap Konsentrasi Polutan Udara', fontsize=20)
fig4.tight_layout(pad=5.0)

ax[0, 0].plot(df.groupby('month')['PM2.5'].mean(), marker='o', linestyle='-', color='b')
ax[0, 0].set_title('PM2.5')
ax[0, 0].set_xlabel('Bulan')
ax[0, 0].set_ylabel('Konsentrasi')

ax[0, 1].plot(df.groupby('month')['PM10'].mean(), marker='o', linestyle='-', color='g')
ax[0, 1].set_title('PM10')
ax[0, 1].set_xlabel('Bulan')
ax[0, 1].set_ylabel('Konsentrasi')

ax[0, 2].plot(df.groupby('month')['SO2'].mean(), marker='o', linestyle='-', color='r')
ax[0, 2].set_title('SO2')
ax[0, 2].set_xlabel('Bulan')
ax[0, 2].set_ylabel('Konsentrasi')

ax[1, 0].plot(df.groupby('month')['NO2'].mean(), marker='o', linestyle='-', color='y')
ax[1, 0].set_title('NO2')
ax[1, 0].set_xlabel('Bulan')
ax[1, 0].set_ylabel('Konsentrasi')

ax[1, 1].plot(df.groupby('month')['CO'].mean(), marker='o', linestyle='-', color='c')
ax[1, 1].set_title('CO')
ax[1, 1].set_xlabel('Bulan')
ax[1, 1].set_ylabel('Konsentrasi')

ax[1, 2].plot(df.groupby('month')['O3'].mean(), marker='o', linestyle='-', color='m')
ax[1, 2].set_title('O3')
ax[1, 2].set_xlabel('Bulan')
ax[1, 2].set_ylabel('Konsentrasi')

st.title('Analisis Kualitas Udara di Beijing')

tab1, tab2 = st.tabs(['Pertanyaan 1', 'Pertanyaan 2'])

with tab1:
    st.subheader('Stasiun apa saja yang memiliki kualitas udara yang buruk dan apa yang menyatakan kualitas udara tersebut buruk sesuai dengan batasan - batasan tertentu yang telah ditetapi oleh satuan kesehatan?')
    st.write('Persentase Konsentrasi Polutan Udara yang Sehat dan Tidak Sehat, Berdasarkan Kota')
    st.pyplot(fig1)

    st.subheader('Konklusi')
    st.markdown(
        '''
        Kota yang sering terjadi polusi adalah sebagai berikut secara berurutan
        1. Aotizhongxin
        2. Huariou
        3. Guanyuan
        4. Wanliu
        5. Shunyi
        6. Dingling
        7. Gucheng
        8. Wanshouxigong
        9. Tiantan
        10. Dongsi
        11. Changping
        12. Nongzhanguan
        ''')

with tab2:
    st.subheader('Apa saja hal - hal yang dapat mempengaruhi kualitas udara berdasarkan data yang ada? baik itu tanggal, waktu, atau faktor cuaca lainnya.')
    st.pyplot(fig2)
    st.pyplot(fig3)
    st.pyplot(fig4)

    correlation_pollutants = df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()
    # show table in streamlit of correlation pollutants
    st.write('Korelasi antar Polutan Udara')
    st.write(correlation_pollutants)
    st.markdown(
        '''
        Dapat disimpulkan dari hasil analisis bahwa korelasi antara beberapa variabel dengan data adalah sebagai berikut:
        - Polutan tinggi pada tiap kota dari jam 0 - 10, kemudian turun dengan titik terendah di jam 15, kemudian naik lagi hingga titik tertinggi di jam 23. Asumsi penulis, hal ini dapat disebabkan karena banyakya kendaraan dan manusia yang beraktifitas di jam - jam tersebut
        - Korelasi antara SO2, NO2, dan CO2 cukup tinggi dengan PM2.5 dan PM10, hal ini dapat dimengerti karena semakin besar polutan yang ada semakin banyak juga partikel yang ada di udara
        ''')
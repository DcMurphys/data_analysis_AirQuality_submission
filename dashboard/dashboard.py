# Import Dependencies 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Create back-end functions 
def create_daily_PM_records_df(df):
    daily_PM_records_df = df.resample(rule='D', on='record_time').agg({
        "station" : "nunique",
        "PM2p5" : "median",
        "PM10" : "median"
    })
    daily_PM_records_df = daily_PM_records_df.reset_index()
    daily_PM_records_df.rename(columns={
        "PM2p5" : "PM2.5"
    }, inplace=True)

    return daily_PM_records_df

def create_daily_other_records_df(df):
    daily_other_records_df = df.resample(rule='D', on='record_time').agg({
        "station" : "nunique",
        "SO2" : "median",
        "NO2" : "median",
        "CO" : "median"
    })
    daily_other_records_df = daily_other_records_df.reset_index()

    return daily_other_records_df
    
def create_daily_AQI_records_df(df):
    daily_AQI_records_df = df.resample(rule='D', on='record_time').agg({
        "station" : "nunique",
        "AQI_result" : "median"
    })
    daily_AQI_records_df = daily_AQI_records_df.reset_index()
   
    return daily_AQI_records_df

def create_daily_AQI_max_records_df(df):
    daily_AQI_max_records_df = df.resample(rule='D', on='record_time').agg({
        "station" : "nunique",
        "AQI_result" : "max"
    })
    daily_AQI_max_records_df = daily_AQI_max_records_df.reset_index()
   
    return daily_AQI_max_records_df

def create_daily_AQIresult_PM2p5_df(df):
    daily_AQIresult_pm2p5_df = df.groupby("record_time").agg({
        "station" : "count",
        "PM2p5" : "median",
        "AQI_result" : "median"
    }).reset_index()
    
    return daily_AQIresult_pm2p5_df

def create_daily_AQIresult_PM10_df(df):
    daily_AQIresult_PM10_df = df.groupby("record_time").agg({
        "station" : "count",
        "PM10" : "median",
        "AQI_result" : "median"
    }).reset_index()
    
    return daily_AQIresult_PM10_df

def create_daily_AQIresult_SO2_df(df):
    daily_AQIresult_SO2_df = df.groupby("record_time").agg({
        "station" : "count",
        "SO2" : "median",
        "AQI_result" : "median"
    }).reset_index()

    return daily_AQIresult_SO2_df

def create_daily_AQIresult_NO2_df(df):
    daily_AQIresult_NO2_df = df.groupby("record_time").agg({
        "station" : "count",
        "NO2" : "median",
        "AQI_result" : "median"
    }).reset_index()
    
    return daily_AQIresult_NO2_df

def create_daily_AQIresult_CO_df(df):
    daily_AQIresult_CO_df = df.groupby("record_time").agg({
        "station" : "count",
        "CO" : "median",
        "AQI_result" : "median"
    }).reset_index()

    return daily_AQIresult_CO_df

# Determining the AQI Status using function 'get_AQI_status '
def get_AQI_status(x):
    if x <= 50:
      return 'Excellent'
    elif x <= 100:
      return 'Good'
    elif x <= 150:
      return 'Lightly Polluted'
    elif x <= 200:
      return 'Moderately Polluted'
    elif x <= 300:
      return 'Heavily Polluted'
    elif x > 300:
      return 'Severely Polluted'
    else:
      return np.NaN


# Loading dataset 'main_data.csv' into new dataframe 'all_record_df'
all_record_df = pd.read_csv("dashboard/main_data.csv")

# Create time widget for data filtering 
datetime_columns = ["record_time"]
all_record_df.sort_values(by="record_time", inplace=True)
all_record_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_record_df[column] = pd.to_datetime(all_record_df[column])

min_time = all_record_df['record_time'].min()
max_time = all_record_df['record_time'].max()

with st.sidebar:
    # Insert application logo
    st.image("dashboard/logo.png", width=128)

    # Get start_time & end_time from date_input
    start_time, end_time = st.date_input(
        label='Time Range',
        min_value=min_time,
        max_value=max_time,
        value=[min_time,max_time]
    )


# Dataframe Variable Instantiation
main_df = all_record_df[(all_record_df["record_time"] >= str(start_time)) & 
                (all_record_df["record_time"] <= str(end_time))]

daily_PM_records_df = create_daily_PM_records_df(main_df)
daily_other_records_df = create_daily_other_records_df(main_df)
daily_AQI_records_df = create_daily_AQI_records_df(main_df)
daily_AQI_max_records_df = create_daily_AQI_max_records_df(main_df)
daily_AQIresult_PM2p5_df = create_daily_AQIresult_PM2p5_df(main_df)
daily_AQIresult_PM10_df = create_daily_AQIresult_PM10_df(main_df)
daily_AQIresult_SO2_df = create_daily_AQIresult_SO2_df(main_df)
daily_AQIresult_NO2_df = create_daily_AQIresult_NO2_df(main_df)
daily_AQIresult_CO_df = create_daily_AQIresult_CO_df(main_df)


# Dashboard Title
st.title('Air Quality Monitoring Dashboard')


# Dashboard Description
st.caption('''Welcome to the Air Quality Monitoring Dashboard App! This app will help you in monitoring the Air Quality Index (AQI) score based on particles like PM2.5, PM10, Sulphur Dioxide (SO2), Nitro Dioxide (NO2), and Carbon Monoxide (CO). The dataset contained in this app have been obtained and analyzed from 12 different stations in China. Determining the AQI status in this app is based on AQI Measuring Standard enforced in China.
''')


# Air Quality Index (AQI) Tracking
st.header("Air Quality Index (AQI) Score")
col1, col2, col3 = st.columns(3, gap="small")

# AQI Metrics 
with col1:
    AQI_result_median = round(daily_AQI_records_df.AQI_result.mean(), 1)
    st.metric("8-hr Avg. AQI Score", value=AQI_result_median)

with col2:
    AQI_result_peak = round(daily_AQI_max_records_df.AQI_result.max(), 2)
    st.metric("Peak AQI Score", value=AQI_result_peak)

with col3:
    AQI_result_status = get_AQI_status(AQI_result_median)
    st.metric("Overall Status", value=AQI_result_status)


fig, ax = plt.subplots()
plt.tight_layout()
plt.tick_params(axis='x', rotation=45)
plt.plot(daily_AQI_records_df['record_time'], daily_AQI_records_df['AQI_result'])
plt.xlabel('Time of recording')
plt.ylabel('AQI score')
st.pyplot(fig)

st.caption("Last time updated: 2017/02/28 23:00:00")

# Tabs for displaying data based on particles 
tab1, tab2, tab3, tab4 = st.tabs(['PM2.5 and PM10', 'Sulphur Dioxide (SO2)', 'Nitro Dioxide (NO2)', 'Carbon Monoxide (CO)'])

# PM2.5 and PM10 Particle Tracking 
with tab1:
    
    st.subheader('PM2.5 and PM10')
    pm2p5_or_pm10 = st.radio(
        label="abc", 
        label_visibility = 'hidden',
        options=('PM2.5', 'PM10', 'Both'),
        horizontal=True
    )
    # Filter based on PM2.5, PM10, and/or both
    if pm2p5_or_pm10 == 'PM2.5':
        st.header("PM2.5-only Particle")
        
        fig, ax = plt.subplots()
        plt.legend(loc='upper left', labels=['PM2.5','PM10'])
        plt.tight_layout()
        plt.tick_params(axis='x', rotation=45)
        plt.plot(daily_PM_records_df['record_time'], daily_PM_records_df['PM2.5'])
        plt.xlabel('Time of recording')
        plt.ylabel('PM2.5 in µg/m3')
        st.pyplot(fig)

    elif pm2p5_or_pm10 == 'PM10':
        st.header("PM10-only Particle")

        fig, ax = plt.subplots()
        plt.legend(loc='upper left', labels=['PM2.5','PM10'])
        plt.tight_layout()
        plt.tick_params(axis='x', rotation=45)
        plt.plot(daily_PM_records_df['record_time'], daily_PM_records_df['PM10'])
        plt.xlabel('Time of recording')
        plt.ylabel('PM10 in µg/m3')
        st.pyplot(fig)

    else:
        st.header("PM2.5 and PM10 Particle")

        fig, ax = plt.subplots()
        plt.tight_layout()
        plt.tick_params(axis='x', rotation=45)
        plt.plot(daily_PM_records_df['record_time'], daily_PM_records_df['PM2.5'], label='PM2.5')
        plt.plot(daily_PM_records_df['record_time'], daily_PM_records_df['PM10'], label='PM10')
        plt.xlabel('Time of recording')
        plt.ylabel('Particulate Matter in µg/m3')
        plt.legend()
        st.pyplot(fig)



# SO2 Particle Tracking
with tab2:
    # Sulphur Dioxide (SO2) 
    st.container()
    st.subheader('Sulphur Dioxide (SO2)')
    # Sulphur Dioxide Particle 
    fig, ax = plt.subplots()
    colors = ['FF6500', '1E3E62']
    ax.plot(daily_other_records_df['record_time'], daily_other_records_df['SO2'])
    ax.tick_params(axis='x', rotation=45)
    ax.set_xlabel('Time of recording')
    ax.set_ylabel('SO2 particle in µg/m3')
    st.pyplot(fig)

    # AQI vs SO2 Correlation  
    st.subheader('Air Quality Index (AQI) vs. Sulphur Dioxide (SO2)')
    fig, ax = plt.subplots()
    colors = ['FF6500', '1E3E62']
    ax.scatter(daily_AQIresult_SO2_df['SO2'], daily_AQIresult_SO2_df['AQI_result'])
    ax.set_xlabel('SO2 particle in µg/m3')
    ax.set_ylabel('AQI score')
    st.pyplot(fig)


# NO2 Particle Tracking
with tab3:
    st.container()
    st.subheader('Air Quality Index (AQI) vs. Nitro Dioxide (NO2)')
    # Nitro Dioxide (NO2)
    fig, ax = plt.subplots()
    colors = ['FF6500', '1E3E62']
    ax.plot(daily_other_records_df['record_time'],daily_other_records_df['NO2'])
    ax.tick_params(axis='x', rotation=45)
    ax.set_xlabel('Time of recording')
    ax.set_ylabel('NO2 particle in µg/m3')
    st.pyplot(fig)

    # AQI vs NO2 Correlation 
    st.subheader('Air Quality Index (AQI) vs. Nitro Dioxide (NO2)')
    fig, ax = plt.subplots()
    colors = ['FF6500', '1E3E62']
    ax.scatter(daily_AQIresult_NO2_df['NO2'],daily_AQIresult_NO2_df['AQI_result'])
    ax.set_xlabel('NO2 particle in µg/m3')
    ax.set_ylabel('AQI score')
    st.pyplot(fig)


# CO Particle Tracking 
with tab4:
    st.container()
    st.subheader('Carbon Monoxide (CO)')
    # Carbon Monoxide (CO)
    fig, ax = plt.subplots()
    colors = ['FF6500', '1E3E62']
    ax.plot(daily_other_records_df['record_time'],daily_other_records_df['CO'])
    ax.tick_params(axis='x', rotation=45)
    ax.set_xlabel('Time of recording')
    ax.set_ylabel('CO particle in µg/m3')
    st.pyplot(fig)

    # AQI vs CO Correlation 
    st.subheader('Air Quality Index (AQI) vs. Carbon Monoxide (NO2)')
    fig, ax = plt.subplots()
    colors = ['FF6500', '1E3E62']
    ax.scatter(daily_AQIresult_CO_df['CO'],daily_AQIresult_CO_df['AQI_result'])
    ax.set_xlabel('CO particle in µg/m3')
    ax.set_ylabel('AQI score')
    st.pyplot(fig)


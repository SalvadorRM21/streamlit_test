import streamlit as st
from collections import namedtuple
import math
import pandas as pd
import numpy as np
import plost                # this package is used to create plots/charts within streamlit
from PIL import Image       # this package is used to put images within streamlit

# Page setting
st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Data
try:
    manual_data = pd.read_excel('data/Cleaned_Manual_Regulation_Final_Two_Days.xlsx', header=0)
    auto_data = pd.read_excel('data/test with automatic heater regulation.xlsx', header=0)

    # Debug: Show column names
    st.write("Manual Data Columns:", manual_data.columns.tolist())
    st.write("Automatic Data Columns:", auto_data.columns.tolist())

    # Adjust column headers if needed
    if 'Current' not in auto_data.columns:
        auto_data.rename(columns={"D7": "Current"}, inplace=True)

    if 'Current (A)' not in manual_data.columns:
        manual_data.rename(columns={"B1": "Current (A)"}, inplace=True)

    # Energy calculation
    voltage = 220
    manual_data["Energy (Wh)"] = manual_data["Current (A)"].astype(float) * voltage * (5 / 3600)
    auto_data["Energy (Wh)"] = auto_data["Current"].astype(float) * voltage * (5 / 3600)

    # Layout: Row A
    st.title("Heater Regulation Dashboard")
    st.markdown("### Compare manual and algorithmic heater regulation with interactive visualizations.")

    # Metrics
    a1, a2 = st.columns(2)
    a1.metric("Manual Total Energy (Wh)", f"{manual_data['Energy (Wh)'].sum():.2f}")
    a2.metric("Automatic Total Energy (Wh)", f"{auto_data['Energy (Wh)'].sum():.2f}")

    # Row B
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("### Manual Energy Distribution")
        plost.bar_chart(
            data=manual_data,
            x='Day',
            y='Energy (Wh)')
    with b2:
        st.markdown("### Automatic Energy Distribution")
        plost.bar_chart(
            data=auto_data,
            x='Day',
            y='Energy (Wh)')

    # Row C
    c1, c2 = st.columns((7, 3))
    with c1:
        st.markdown("### Heatmap of Temperature (Manual)")
        plost.time_hist(
            data=manual_data,
            date='Timestamp',
            x_unit='hour',
            y_unit='day',
            color='Temperature (°C)',
            aggregate='median',
            legend=None)
    with c2:
        st.markdown("### Heatmap of Temperature (Automatic)")
        plost.time_hist(
            data=auto_data,
            date='Timestamp',
            x_unit='hour',
            y_unit='day',
            color='Temperature (°C)',
            aggregate='median',
            legend=None)

    # Data Previews
    st.markdown("### Data Previews")
    with st.expander("Manual Regulation Data"):
        st.dataframe(manual_data.head(20))
    with st.expander("Automatic Regulation Data"):
        st.dataframe(auto_data.head(20))

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")




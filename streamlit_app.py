import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page settings
st.set_page_config(layout="wide", page_title="Heater Regulation Dashboard")

# Title
st.title("Heater Regulation Dashboard")
st.markdown("### Compare manual and algorithmic heater regulation with interactive visualizations.")

# File paths
manual_file_url = 'data/Cleaned_Manual_Regulation_Final_Two_Days.xlsx'
auto_file_url = 'data/test with automatic heater regulation.xlsx'

try:
    # Read the data
    manual_data = pd.read_excel(manual_file_url)
    auto_data = pd.read_excel(auto_file_url)

    # Energy calculation
    voltage = 220
    manual_data["Energy (Wh)"] = manual_data["Current (A)"] * voltage * (5 / 3600)
    auto_data["Energy (Wh)"] = auto_data["RMS Current (A)"] * voltage * (5 / 3600)

    manual_total_energy = manual_data["Energy (Wh)"].sum()
    auto_total_energy = auto_data["Energy (Wh)"].sum()

    manual_on_time = manual_data[manual_data["Current (A)"] > 0].shape[0] * 5 / 60  # Minutes
    auto_on_time = auto_data[auto_data["RMS Current (A)"] > 0].shape[0] * 5 / 60  # Minutes

    # Layout: Metrics
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Manual Energy (Wh)", f"{manual_total_energy:.2f}")
    col2.metric("Auto Energy (Wh)", f"{auto_total_energy:.2f}")
    col3.metric("Manual On-Time (min)", f"{manual_on_time:.2f}")
    col4.metric("Auto On-Time (min)", f"{auto_on_time:.2f}")

    # Layout: Charts
    st.markdown("### Energy Consumption Comparison")
    energy_data = pd.DataFrame({
        "Type": ["Manual", "Automatic"],
        "Total Energy (Wh)": [manual_total_energy, auto_total_energy]
    })
    fig_energy = px.bar(energy_data, x="Type", y="Total Energy (Wh)", color="Type",
                        title="Energy Consumption (Manual vs Automatic)", text="Total Energy (Wh)")
    st.plotly_chart(fig_energy, use_container_width=True)

    st.markdown("### Heater On-Time Comparison")
    on_time_data = pd.DataFrame({
        "Type": ["Manual", "Automatic"],
        "On-Time (minutes)": [manual_on_time, auto_on_time]
    })
    fig_on_time = px.bar(on_time_data, x="Type", y="On-Time (minutes)", color="Type",
                         title="Heater On-Time (Manual vs Automatic)", text="On-Time (minutes)")
    st.plotly_chart(fig_on_time, use_container_width=True)

    st.markdown("### Temperature Over Time")
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(y=manual_data["Temperature (°C)"], mode='lines', name='Manual'))
    fig_temp.add_trace(go.Scatter(y=auto_data["Temperature (°C)"], mode='lines', name='Automatic'))
    fig_temp.update_layout(title="Temperature Comparison (Manual vs Automatic)",
                           xaxis_title="Time", yaxis_title="Temperature (°C)",
                           legend=dict(orientation="h"))
    st.plotly_chart(fig_temp, use_container_width=True)

except FileNotFoundError as e:
    st.error(f"Error: {e}. Please ensure the data files are in the correct directory.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")





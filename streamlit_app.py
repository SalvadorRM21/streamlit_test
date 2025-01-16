import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Page settings
st.set_page_config(layout="wide", page_title="Heater Regulation Dashboard")

# Title
st.title("Heater Regulation Dashboard")
st.markdown("This dashboard compares manual and algorithmic heater regulation.")

# Load data
# Upload files
manual_file = st.file_uploader("Upload Manual Regulation Data", type=["xlsx"])
auto_file = st.file_uploader("Upload Automatic Regulation Data", type=["xlsx"])

if manual_file and auto_file:
    # Read the data
    manual_data = pd.read_excel(manual_file)
    auto_data = pd.read_excel(auto_file)

    # Preprocessing
    st.subheader("Data Previews")
    st.write("**Manual Regulation Data:**")
    st.write(manual_data.head())

    st.write("**Automatic Regulation Data:**")
    st.write(auto_data.head())

    # Energy consumption calculation
    st.subheader("Energy Consumption Comparison")
    voltage = 220  # Assuming 220V

    # Manual energy
    manual_data["Energy (Wh)"] = manual_data["Current (A)"] * voltage * (5 / 3600)
    manual_total_energy = manual_data["Energy (Wh)"].sum()

    # Automatic energy
    auto_data["Energy (Wh)"] = auto_data["RMS Current (A)"] * voltage * (5 / 3600)
    auto_total_energy = auto_data["Energy (Wh)"].sum()

    # Display energy comparison
    st.metric(label="Total Energy (Manual)", value=f"{manual_total_energy:.2f} Wh")
    st.metric(label="Total Energy (Automatic)", value=f"{auto_total_energy:.2f} Wh")

    # Plot energy consumption
    energy_data = pd.DataFrame({
        "Type": ["Manual", "Automatic"],
        "Total Energy (Wh)": [manual_total_energy, auto_total_energy]
    })

    fig_energy = px.bar(energy_data, x="Type", y="Total Energy (Wh)", title="Energy Consumption (Manual vs Automatic)",
                        color="Type", text="Total Energy (Wh)")
    st.plotly_chart(fig_energy)

    # Heater On-Time Comparison
    st.subheader("Heater On-Time Comparison")
    manual_on_time = manual_data[manual_data["Current (A)"] > 0].shape[0] * 5 / 60  # Minutes
    auto_on_time = auto_data[auto_data["RMS Current (A)"] > 0].shape[0] * 5 / 60  # Minutes

    st.metric(label="Heater On-Time (Manual)", value=f"{manual_on_time:.2f} minutes")
    st.metric(label="Heater On-Time (Automatic)", value=f"{auto_on_time:.2f} minutes")

    # Plot On-Time
    on_time_data = pd.DataFrame({
        "Type": ["Manual", "Automatic"],
        "On-Time (minutes)": [manual_on_time, auto_on_time]
    })

    fig_on_time = px.bar(on_time_data, x="Type", y="On-Time (minutes)",
                         title="Heater On-Time (Manual vs Automatic)",
                         color="Type", text="On-Time (minutes)")
    st.plotly_chart(fig_on_time)

    # Temperature Comparison
    st.subheader("Temperature Comparison")
    fig_temp = plt.figure(figsize=(10, 5))
    sns.lineplot(data=manual_data, x=manual_data.index, y="Temperature (°C)", label="Manual")
    sns.lineplot(data=auto_data, x=auto_data.index, y="Temperature (°C)", label="Automatic")
    plt.title("Temperature Over Time (Manual vs Automatic)")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    st.pyplot(fig_temp)

else:
    st.info("Please upload both manual and automatic regulation data to proceed.")

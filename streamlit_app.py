# Full-width layout for the plots
st.set_page_config(layout="wide")

# Single-column layout to give more width
st.markdown("<h1 style='text-align: center; color: white;'>ThermoScope</h1>", unsafe_allow_html=True)

st.markdown("---")  # Add a separator for better spacing

# December 7th 2024 graph
st.header("December 7th 2024")
fig_7, ax_7 = plt.subplots(figsize=(16, 8))  # Wider and taller figure
fig_7.patch.set_facecolor('none')  # Transparent figure background
ax_7.set_facecolor((0, 0, 0, 0))  # Transparent axes background
ax_7.plot(df_7["Hour"], df_7["Temperature"], label="Temperature", color="blue")
ax_7.set_xlabel("Hour")
ax_7.set_ylabel("Temperature (°C)")
ax_7.set_title("Outside Temperature")
plt.xticks(rotation=45)
st.pyplot(fig_7, use_container_width=True)  # Expand graph width

st.metric(label="Electricity Price (€/kWh) for December 7th 2024", value=f"{price_7} €")

st.markdown("---")  # Separator between graphs

# December 8th 2024 graph
st.header("December 8th 2024")
fig_8, ax_8 = plt.subplots(figsize=(16, 8))  # Wider and taller figure
fig_8.patch.set_facecolor('none')  # Transparent figure background
ax_8.set_facecolor((0, 0, 0, 0))  # Transparent axes background
ax_8.plot(df_8["Hour"], df_8["Temperature"], label="Temperature", color="orange")
ax_8.set_xlabel("Hour")
ax_8.set_ylabel("Temperature (°C)")
ax_8.set_title("Outside Temperature")
plt.xticks(rotation=45)
st.pyplot(fig_8, use_container_width=True)  # Expand graph width

st.metric(label="Electricity Price (€/kWh) for December 8th 2024", value=f"{price_8} €")





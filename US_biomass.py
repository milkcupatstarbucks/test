import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Load latitude and longitude data
lonlat = np.load('lonlat.npz')['lonlat']
lon = lonlat[:, 0]
lat = lonlat[:, 1]

# Load the associated values (e.g., emissions, temperatures, etc.)
data = np.load('y_all.npz')['y_all']

# Create a DataFrame with lat, lon, and associated values
df = pd.DataFrame({
    "lat": lat,
    "lon": lon,
    "value": data,  # Replace with your specific value column
})

# Normalize the 'value' column to a range of 0-255 for RGB scaling
df['normalized_value'] = ((df['value'] - df['value'].min()) / 
                          (df['value'].max() - df['value'].min()) * 255).astype(int)

# Define color scale: Map normalized values to colors (e.g., blue to red)
def get_color(value):
    """Assign a color based on the normalized value."""
    # Example: Blue for low values, red for high values
    return [value, 255 - value, 150]  # RGB values; modify as needed

# Apply color mapping to each row
df['color'] = df['normalized_value'].apply(get_color)

# Define the Pydeck layer with data points and dynamic colors
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["lon", "lat"],
    get_radius=20000,  # Adjust radius based on your needs
    get_fill_color="color",  # Use the 'color' column for fill color
    pickable=True,  # Enable picking (clicking) on points
)

# Define Pydeck view (map view)
view_state = pdk.ViewState(
    latitude=np.mean(lat),
    longitude=np.mean(lon),
    zoom=3,  # Adjust zoom level based on your data
    pitch=50,  # Optional: tilt the map for a 3D effect
)

# Create the Pydeck chart with the defined layer and view state
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Value: {value}"},  # Show value on hover
)

# Display the map with the Pydeck chart
st.pydeck_chart(deck)

# Optional: Display the DataFrame with additional information
st.write("Data with color mapping:", df)

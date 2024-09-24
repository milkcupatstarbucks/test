import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Title of the app
st.title('Heatmap of a Random 2D Array')

# Generate a random 2D array
array_size = st.slider('Select array size', 5, 50, 10)  # Slider for array size
random_array = np.random.rand(array_size, array_size)

# Display the random array as a heatmap
st.write('Random 2D Array:')
st.write(random_array)

# Plot the heatmap
fig, ax = plt.subplots()
sns.heatmap(random_array, ax=ax, cmap='viridis')

# Display the heatmap
st.pyplot(fig)
import streamlit as st
import plotly.express as plotly
import numpy as np

st.title("Production Possibility Curves")
st.sidebar.header("Settings")
L = st.sidebar.slider("Total Labour", 10, 100, 50, step=10)
e_x = st.sidebar.slider("efficiency of oranges", 1, 10, 5, step=1)
e_y = st.sidebar.slider("efficiency of frogs", 1, 10, 5, step=1)

x = np.arange(0,10,0.1)
y = e_y*np.sqrt(L-(x/e_x)**2)

fig = plotly.line(x=x,y=y)
fig.update_layout(
       xaxis_range=[0, 30],  # Set x-axis range from 0 to 4
       yaxis_range=[0, 30],   # Set y-axis range from 0 to 7
       width=100,  # Set a fixed width in pixels
       height=100  # Set a fixed height in pixels
   )
st.plotly_chart(fig)


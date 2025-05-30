import streamlit as st
import plotly.express as plotly
import numpy as np

st.title("Production Possibility Curves")
st.sidebar.header("Settings")
L = st.sidebar.slider("Total Labour", 10, 100, 50, step=10)
e_x = st.sidebar.slider("efficiency of frogs", 1, 10, 5, step=1)
e_y = st.sidebar.slider("efficiency of oranges", 1, 10, 5, step=1)

frogs = np.arange(0,200,1)
oranges = e_y*np.sqrt(L-(frogs/e_x)**2)

fig = plotly.line(x=frogs,y=oranges)
fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True
fig.update_layout(
       xaxis_range=[0, 20],  # Set x-axis range from 0 to 4
       yaxis_range=[0, 20],   # Set y-axis range from 0 to 7
       width=600,  # Set a fixed width in pixels
       height=800  # Set a fixed height in pixels
   )
st.plotly_chart(fig)


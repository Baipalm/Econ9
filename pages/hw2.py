import streamlit as st
import plotly.express as plotly
import numpy as np
import pandas as pd

st.title("Production Possibility Curves")
st.sidebar.header("Settings")
L = st.sidebar.slider("Labour", min_value=1, max_value=50, value=25, step=1)
st.sidebar.subheader("Production Efficiency")
e_x = st.sidebar.slider("🐸", 1, 5, 2.5, step=0.5)
e_y = st.sidebar.slider("🟠", 1, 5, 2.5, step=0.5)

frogs = np.arange(0,30,0.1)
oranges = e_y*np.sqrt(L-(frogs/e_x)**2)
data = np.hstack((frogs,oranges))
# fig = plotly.line(x=frogs,y=oranges)
# fig.layout.xaxis.fixedrange = True
# fig.layout.yaxis.fixedrange = True
st.line_chart(oranges, x_label="🐸", y_label="🟠",use_container_width=True)


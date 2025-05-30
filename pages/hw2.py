import streamlit as st
import plotly.express as plotly
import numpy as np

st.title("Production Possibility Curves")
st.sidebar.header("NMF Convergence Settings")
L = st.sidebar.slider("Total Labour", 10, 100, 50, step=10)
e_x = st.sidebar.slider("efficiency of oranges", 1, 20, 6, step=1)
e_y = st.sidebar.slider("efficiency of frogs", 1, 20, 10, step=1)

x = np.arange(0,10,0.1)
y = e_y*np.sqrt(L-(x/e_x)**2)

fig = plotly.line(x=x,y=y)

st.plotly_chart(fig)


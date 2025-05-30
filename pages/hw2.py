import streamlit as st
import plotly.express as plotly
import numpy as np
import pandas as pd

st.title("Production Possibility Curves")
st.sidebar.header("Settings")
L = st.sidebar.slider("Total Labour", 10, 100, 50, step=10)
e_x = st.sidebar.slider("efficiency of frogs", 1, 10, 5, step=1)
e_y = st.sidebar.slider("efficiency of oranges", 1, 10, 5, step=1)

frogs = np.arange(0,40,0.1)
oranges = e_y*np.sqrt(L-(frogs/e_x)**2)
chart_data = pd.DataFrame(
    {
        "col1": frogs,
        "col2": oranges,
    }
)
# fig = plotly.line(x=frogs,y=oranges)
# fig.layout.xaxis.fixedrange = True
# fig.layout.yaxis.fixedrange = True
st.line_chart(chart_data, x="frogs", y="oranges")


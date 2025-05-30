import streamlit as st
import plotly.express as plotly
import numpy as np
import pandas as pd
import altair as alt
st.title("Production Possibility Curves")
st.sidebar.header("Settings")
L = st.sidebar.slider("Labour", min_value=1, max_value=40, value=15, step=1)
st.sidebar.subheader("Production Efficiency")
e_x = st.sidebar.slider("🐸", 1, 20, 5, step=1)
e_y = st.sidebar.slider("🟠", 1, 20, 5, step=1)
max_frogs = np.sqrt(40)*20
frogs = np.arange(0, max_frogs, 0.05)
oranges = e_y*np.sqrt(L-(frogs/e_x)**2)
data = np.hstack((frogs,oranges))
df = pd.DataFrame({
        'x': frogs,
        'y': oranges
    })

chart = alt.Chart(df).mark_line().encode(
    alt.X('x:Q', scale=alt.Scale(domain=[0, max_frogs*1.1]), title='🐸'),
    alt.Y('y:Q', scale=alt.Scale(domain=[0, max_frogs*1.1]), title='🟠'),
)
st.altair_chart(chart.properties(width=600, height=600)) 

# fig = plotly.line(x=frogs,y=oranges)
# fig.layout.xaxis.fixedrange = True
# fig.layout.yaxis.fixedrange = True
#st.line_chart(oranges, x_label="🐸", y_label="🟠",use_container_width=True)


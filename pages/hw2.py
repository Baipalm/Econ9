import streamlit as st
import plotly.express as exp
import plotly.graph_objects as go
import numpy as np
#import matplotlib.pyplot as plt 
#import plotly.tools as tls
import pandas as pd
#import altair as alt
st.title("Production Possibility Curves")
st.sidebar.header("Settings")
L = st.sidebar.slider("Labour", min_value=1, max_value=40, value=20, step=1)
st.sidebar.subheader("Production Efficiency")
e_x = st.sidebar.slider("🐸", 1, 20, 10, step=1)
e_y = st.sidebar.slider("🟠", 1, 20, 10, step=1)
max_frogs = np.sqrt(40)*20
frogs = np.arange(0, max_frogs, 0.05)
np.append(frogs,e_x*np.sqrt(L))
oranges = e_y*np.sqrt(L-(frogs/e_x)**2)
np.append(oranges,0)
data = np.hstack((frogs,oranges))
df = pd.DataFrame({
        'x': frogs,
        'y': oranges
    })

#def abline(slope, intercept):
#    """Plot a line from slope and intercept"""
#    axes = plt.gca()
#    x_vals = np.array(axes.get_xlim())
#    y_vals = intercept + slope * x_vals
#    plt.plot(x_vals, y_vals, '--')
#chart = alt.Chart(df).mark_line().encode(
#    alt.X('x:Q', scale=alt.Scale(domain=[0, max_frogs*1.01]), title='🐸'),
#    alt.Y('y:Q', scale=alt.Scale(domain=[0, max_frogs*1.01]), title='🟠'),
#)
#x = st.slider("movement along the curve", min_value=0, max_value=max_frogs, value=10, step=0.05)
#slope = oranges/x
#fig_mpl = abline(slope,intercept)
#st.altair_chart(chart.properties(width=600, height=600),use_container_width=True) 
fig = go.Figure()
fig.update_layout(
    xaxis=dict(range=[0, 130]),  # Set x-axis range from 0 to 6
    yaxis=dict(range=[0, 130])   # Set y-axis range from 5 to 20
)
fig.update_layout(
    xaxis_title="# of 🐸 ",
    yaxis_title="# of 🟠"
)
fig.add_trace(
        go.Scatter(x=df['x'], y=df['y'],mode='lines', fill='tozeroy')
)

fig.update_yaxes(fixedrange=True)
fig.update_xaxes(fixedrange=True)
#fig.update_traces(
#    text=[f'🐸: {x_val}, 🟠: {y_val}' for x_val, y_val in zip(frogs, oranges)],
#    hovertemplate="<b>%{text}</b><extra></extra>"
#)

fig.update_layout(width=800, height=800)
#fig = plotly.line(x=frogs,y=oranges)
#fig= go.Figure(data = [trace1,trace2],layout_xaxis_range=[0,np.sqrt(40)*20*1.1],layout_yaxis_range=[0,np.sqrt(40)*20*1.1])

st.plotly_chart(fig, use_container_width=True, selection_mode=('points'))
#st.line_chart(oranges, x_label="🐸", y_label="🟠",use_container_width=True)

  





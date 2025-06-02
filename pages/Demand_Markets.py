import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configure the Streamlit page
st.set_page_config(page_title="Linear Demand Curve", layout="centered")

st.title("Linear Demand Curve")

# Generate x (quantity) and y (price) values for a downward‐sloping demand line
x = np.linspace(0, 10, 100)
y = -x + 10  # Demand: Price = -Quantity + 10

# Create Plotly figure with the area under the demand curve filled
fig = go.Figure(
    data=go.Scatter(
        x=x,
        y=y,
        mode="lines",
        fill="tozeroy",               # fills area down to y=0
        line=dict(color="crimson"),
        name="Demand: P = -Q + 10"
    )
)

# Configure axes range and disable zoom/pan for a fixed, symmetric view
fig.update_layout(
    xaxis=dict(
        title="Quantity Demanded",
        range=[0, 10],
        fixedrange=True  # disables zoom/pan on x-axis
    ),
    yaxis=dict(
        title="Price",
        range=[0, 10],
        fixedrange=True  # disables zoom/pan on y-axis
    ),
    margin=dict(l=40, r=40, t=40, b=40),
    showlegend=False
)

# Render the figure to the Streamlit app (the website)
st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})

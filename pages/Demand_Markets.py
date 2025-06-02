import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("Price vs. Quantity Demanded")

# Generate x and y values
x = np.linspace(0, 10, 100)
y = x / 2 + 5

# Create Plotly figure with filled area under the curve
fig = go.Figure(
    data=go.Scatter(
        x=x,
        y=y,
        mode="lines",
        fill="tozeroy",
        line=dict(color="royalblue"),
        name="Price = Quantity/2 + 5"
    )
)

# Configure axes range and disable zoom/pan
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

# Disable all interactivity (no scroll, no zoom, no pan)
st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})


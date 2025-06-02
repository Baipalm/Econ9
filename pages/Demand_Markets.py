import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Title
st.title("Impact of Demand Shifts vs. Movement Along Demand Curve on Two Correlated Markets")

# Parameters
max_quantity = 10
base_b = max_quantity * 0.5  # intercept of demand curve
x_vals = np.linspace(0, max_quantity, 200)

# Base (linear) demand curve: P = -1/2 * Q + b
base_price_vals = -0.5 * x_vals + base_b

# Compute the “center” point on the base curve
x_center = max_quantity / 2
initial_price = -0.5 * x_center + base_b  # = max_quantity / 4

# Sidebar controls
st.sidebar.header("Controls")
relationship = st.sidebar.selectbox(
    "Choose Market Relationship",
    ("Complementary", "Substitute")
)

slider_price = st.sidebar.slider(
    "Left‐Market Price (move the point up/down)",
    min_value=0.0,
    max_value=float(base_b),
    value=float(initial_price),
    step=0.1
)

# Compute left‐market point: movement along the original demand curve
# Given P_left = slider_price, solve for Q_left on P = -0.5 Q + b  => Q = 2*(b - P)
q_left = 2 * (base_b - slider_price)
p_left = slider_price

# Compute how the right‐market intercept (b_right) shifts
delta_price = slider_price - initial_price
if relationship == "Complementary":
    # If left price ↑, right demand ↓ ⇒ subtract delta_price from intercept
    b_right = base_b - delta_price
else:
    # Substitute: if left price ↑, right demand ↑ ⇒ add delta_price to intercept
    b_right = base_b + delta_price

# Right‐market demand curve (shifted): P = -0.5 Q + b_right
price_vals_right = -0.5 * x_vals + b_right
# Ensure the shifted curve stays within the plotting range
# (Clip intercept if it goes out of bounds)
b_right = max(0.0, min( max_quantity*0.75, b_right))  
price_vals_right = -0.5 * x_vals + b_right

# Right‐market point: hold P_right = slider_price, solve Q_right on shifted curve
q_right = 2 * (b_right - slider_price)
p_right = slider_price

# Create side‐by‐side Plotly figure
fig = make_subplots(rows=1, cols=2, subplot_titles=("Left Market", "Right Market"))

# LEFT MARKET: Original demand curve + movement‐point
fig.add_trace(
    go.Scatter(
        x=x_vals,
        y=base_price_vals,
        mode="lines",
        name="Demand Curve",
        line=dict(color="blue")
    ),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=[q_left],
        y=[p_left],
        mode="markers",
        name="Current Point",
        marker=dict(color="red", size=10)
    ),
    row=1, col=1
)

# RIGHT MARKET: Shifted demand curve + resulting point
fig.add_trace(
    go.Scatter(
        x=x_vals,
        y=price_vals_right,
        mode="lines",
        name="Shifted Demand Curve",
        line=dict(color="green")
    ),
    row=1, col=2
)
fig.add_trace(
    go.Scatter(
        x=[q_right],
        y=[p_right],
        mode="markers",
        name="Resulting Point",
        marker=dict(color="orange", size=10)
    ),
    row=1, col=2
)

# Update axes: fixed ranges, labels
for i in (1, 2):
    fig.update_xaxes(
        title_text="Quantity Demanded",
        range=[0, max_quantity],
        fixedrange=True,
        row=1, col=i
    )
    fig.update_yaxes(
        title_text="Price",
        range=[0, base_b],
        fixedrange=True,
        row=1, col=i
    )

# Layout adjustments
fig.update_layout(
    height=500,
    width=900,
    showlegend=False,
    margin=dict(l=40, r=40, t=60, b=40),
)

st.plotly_chart(fig, use_container_width=True)


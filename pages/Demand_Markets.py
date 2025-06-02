import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Title
st.title("Impact of Demand Shifts vs. Movement Along Demand Curve on Two Correlated Markets")

# PARAMETERS
max_quantity = 20                     # (4) Increase max quantity range to 20
base_b = max_quantity * 0.5           # intercept of the demand curve (so base_b = 10)
x_vals = np.linspace(0, max_quantity, 200)

# Base (linear) demand curve: P = -0.5 * Q + b
base_price_vals = -0.5 * x_vals + base_b

# Compute the “center” point on the base curve (used as the initial reference)
x_center = max_quantity / 2           # = 10
initial_price = -0.5 * x_center + base_b  # = -0.5 * 10 + 10 = 5

# SIDEBAR: slider now controls quantity on the left‐market curve
st.sidebar.header("Controls")
relationship = st.sidebar.selectbox(
    "Choose Market Relationship",
    ("Complementary", "Substitute")
)

slider_q_left = st.sidebar.slider(
    "Left‐Market Quantity (move the point left/right)",
    min_value=0.0,
    max_value=float(max_quantity),
    value=float(x_center),
    step=0.1
)

# 2. Compute left‐market point by moving horizontally along the demand curve:
q_left = slider_q_left
p_left = -0.5 * q_left + base_b

# 3. Compute how the right‐market intercept (b_right) shifts based on delta_price
delta_price = p_left - initial_price

if relationship == "Complementary":
    # If left price ↑ ⇒ right demand ↓ ⇒ subtract delta_price from intercept
    b_right = base_b - delta_price
else:
    # Substitute: if left price ↑ ⇒ right demand ↑ ⇒ add delta_price to intercept
    b_right = base_b + delta_price

# Clip b_right so that the right‐curve doesn’t go outside plotting bounds (0 to 20)
b_right = max(0.0, min(20.0, b_right))
price_vals_right = -0.5 * x_vals + b_right

# Right‐market point: hold P_right = p_left, solve Q_right on shifted curve
q_right = 2 * (b_right - p_left)
p_right = p_left

# 5. Compute changes (deltas) relative to the fixed yellow (initial) point
delta_q_left = q_left - x_center
delta_p_left = p_left - initial_price

delta_q_right = q_right - x_center
delta_p_right = p_right - initial_price

# DISPLAY THE NUMERIC “CHANGE” METRICS AT THE TOP RIGHT
# We'll create three columns and put the metrics in the rightmost one.
col1, col2, col3 = st.columns([1, 3, 1])
with col3:
    st.markdown("**Δ Left‐Market vs. Initial**")
    st.markdown(f"- ΔQ_left = {delta_q_left:.2f}")
    st.markdown(f"- ΔP_left = {delta_p_left:.2f}")
    st.markdown("**Δ Right‐Market vs. Initial**")
    st.markdown(f"- ΔQ_right = {delta_q_right:.2f}")
    st.markdown(f"- ΔP_right = {delta_p_right:.2f}")

# CREATE SIDE‐BY‐SIDE PLOTLY FIGURE
fig = make_subplots(rows=1, cols=2, subplot_titles=("Left Market", "Right Market"))

# LEFT MARKET:
#  - Filled‐in demand curve (blue)
#  - Fixed yellow point at (x_center, initial_price)
#  - Current point (red)
fig.add_trace(
    go.Scatter(
        x=x_vals,
        y=base_price_vals,
        mode="lines",
        name="Demand Curve",
        line=dict(color="blue"),
        fill="tozeroy",
        fillcolor="rgba(173, 216, 230, 0.3)"
    ),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=[x_center],
        y=[initial_price],
        mode="markers",
        name="Initial (Yellow)",
        marker=dict(color="yellow", size=10)
    ),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=[q_left],
        y=[p_left],
        mode="markers",
        name="Current (Red)",
        marker=dict(color="red", size=10)
    ),
    row=1, col=1
)

# RIGHT MARKET:
#  - Shifted demand curve (green) with fill
#  - Fixed yellow point at (x_center, initial_price)
#  - Resulting point (orange)
fig.add_trace(
    go.Scatter(
        x=x_vals,
        y=price_vals_right,
        mode="lines",
        name="Shifted Demand Curve",
        line=dict(color="green"),
        fill="tozeroy",
        fillcolor="rgba(144, 238, 144, 0.3)"
    ),
    row=1, col=2
)
fig.add_trace(
    go.Scatter(
        x=[x_center],
        y=[initial_price],
        mode="markers",
        name="Initial (Yellow)",
        marker=dict(color="yellow", size=10)
    ),
    row=1, col=2
)
fig.add_trace(
    go.Scatter(
        x=[q_right],
        y=[p_right],
        mode="markers",
        name="Resulting (Orange)",
        marker=dict(color="orange", size=10)
    ),
    row=1, col=2
)

# UPDATE AXES: fixed ranges (0 to 20), labels
for i in (1, 2):
    fig.update_xaxes(
        title_text="Quantity Demanded",
        range=[0, 20],
        fixedrange=True,
        row=1, col=i
    )
    fig.update_yaxes(
        title_text="Price",
        range=[0, 20],
        fixedrange=True,
        row=1, col=i
    )

# LAYOUT ADJUSTMENTS
fig.update_layout(
    height=500,
    width=900,
    showlegend=False,
    margin=dict(l=40, r=40, t=60, b=40),
)

# RENDER IN STREAMLIT
st.plotly_chart(fig, use_container_width=True)

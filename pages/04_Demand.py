import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ----------------------------------------
# 1) Set up wide layout and page title
st.set_page_config(page_title="Interactive Demand Curve", layout="wide")
st.title("Demand Curve with Movable Point and Vertical Shift")

# ----------------------------------------
# 2) Persist slider values in session_state (movement and shift)
if "x_pos" not in st.session_state:
    st.session_state.x_pos = 2.5
if "vertical_shift" not in st.session_state:
    st.session_state.vertical_shift = 0.0

# ----------------------------------------
# 3) Sliders: one for horizontal movement, one for vertical shift
x_pos = st.slider(
    label="Quantity (Move Point Horizontally)",
    min_value=0.0,
    max_value=5.0,
    value=st.session_state.x_pos,
    step=0.1,
    key="x_pos"
)

vertical_shift = st.slider(
    label="Vertical Shift of Curve (ΔP)",
    min_value=-5.0,
    max_value=5.0,
    value=st.session_state.vertical_shift,
    step=0.1,
    key="vertical_shift"
)

# ----------------------------------------
# 4) Compute the two curves and the single dot
# Original demand:     P = –Q + 5
# Shifted demand:      P = –Q + (5 + vertical_shift)
x_vals = np.linspace(0, 10, 100)
y_original = -x_vals + 5
intercept_shifted = 5.0 + vertical_shift
y_shifted = -x_vals + intercept_shifted

# Dot is placed on the shifted curve at x = x_pos
x_dot = x_pos
y_dot = -x_pos + intercept_shifted

# ----------------------------------------
# 5) Build a single Plotly figure with both curves + 1 dot
fig = go.Figure()

# 5a) Original demand curve (crimson fill)
fig.add_trace(
    go.Scatter(
        x=x_vals,
        y=y_original,
        mode="lines",
        fill="tozeroy",
        line=dict(color="crimson"),
        name="Original: P = –Q + 5"
    )
)

# 5b) Shifted demand curve (navy fill)
fig.add_trace(
    go.Scatter(
        x=x_vals,
        y=y_shifted,
        mode="lines",
        fill="tozeroy",
        line=dict(color="navy"),
        name=f"Shifted: P = –Q + {intercept_shifted:.2f}"
    )
)

# 5c) Single red dot at (x_dot, y_dot)
fig.add_trace(
    go.Scatter(
        x=[x_dot],
        y=[y_dot],
        mode="markers",
        marker=dict(color="red", size=12),
        name="Movable Point"
    )
)

# 5d) Update layout so both curves share axes
fig.update_layout(
    title="Demand Curve with Movable Point and Vertical Shift",
    xaxis=dict(title="Quantity Demanded", range=[0, 10], fixedrange=True),
    yaxis=dict(title="Price",              range=[0, 10], fixedrange=True),
    width=800,
    height=500,
    margin=dict(l=40, r=40, t=50, b=40),
    legend=dict(x=0.02, y=0.98),
)

# ----------------------------------------
# 6) Display the combined figure
st.plotly_chart(
    fig,
    use_container_width=False,
    config={"staticPlot": True},
    key="combined_demand_curve"
)

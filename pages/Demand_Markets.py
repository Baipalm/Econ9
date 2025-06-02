import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1) Wide layout
st.set_page_config(page_title="Interactive Demand Curves", layout="wide")

st.title("Side-by-Side Demand Curves with Movable Left Marker")

# ------------------------------------------------------------------------------
# 2) Slider: controls the left‐hand point (and also the shift amount for the right)
x_left = st.slider(
    label="Move Left Circle (Quantity)", 
    min_value=0.0, 
    max_value=5.0, 
    value=2.5, 
    step=0.1
)
# The corresponding price on the original demand curve P = -Q + 5:
y_left = -x_left + 5

# Compute the horizontal shift for the right‐hand curve.
# Original "center" was at Q = 2.5.  Whenever x_left moves,
# we set Δ = x_left - 2.5, and shift the right curve by Δ.
delta = x_left - 2.5

# ------------------------------------------------------------------------------
# 3) Build a function that draws a demand curve plus a red marker.
#    We will call it twice: once for the LEFT (no shift), once for the RIGHT (with shift).

# Prepare 100 points in [0,5] for plotting.
x_vals = np.linspace(0, 5, 100)

def create_shifted_demand_figure(shift: float, marker_x: float, marker_y: float, title: str):
    """
    - shift: how much to shift horizontally (positive = shift right, negative = shift left).
             In practice, we implement P = - (Q - shift) + 5  <=>  P = -Q + (5 + shift).
    - marker_x, marker_y: coordinates at which to draw the red circle (fixed).
    - title: subtitle for the figure.
    """
    # Because shifting horizontally by `shift` is the same as raising the intercept from 5 to (5+shift):
    intercept = 5.0 + shift
    # New demand line: P = - x_vals + intercept
    y_vals_shifted = -x_vals + intercept

    fig = go.Figure()

    # 3a) Plot the (possibly shifted) demand line, filled under the curve:
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals_shifted,
            mode="lines",
            fill="tozeroy",
            line=dict(color="crimson"),
            name=f"Demand (shifted) if Δ={shift:+.2f}"
        )
    )

    # 3b) Plot the red circle at (marker_x, marker_y):
    fig.add_trace(
        go.Scatter(
            x=[marker_x],
            y=[marker_y],
            mode="markers",
            marker=dict(color="red", size=12),
            showlegend=False
        )
    )

    # 3c) Fix axes so they stay square, disable zoom/pan, etc.
    fig.update_layout(
        title=title,
        xaxis=dict(
            title="Quantity Demanded",
            range=[0, 5],
            fixedrange=True
        ),
        yaxis=dict(
            title="Price",
            range=[0, 5],
            fixedrange=True
        ),
        width=400,
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )

    return fig

# ------------------------------------------------------------------------------
# 4) Create the two figures:
#    - LEFT: shift = 0 (i.e. original demand) + moving marker (x_left, y_left)
#    - RIGHT: shift = delta, but marker fixed at (2.5, 2.5)

fig_left = create_shifted_demand_figure(
    shift=0.0,
    marker_x=x_left,
    marker_y=y_left,
    title="Left Curve (Movable Marker)"
)

fig_right = create_shifted_demand_figure(
    shift=delta,
    marker_x=2.5,       # fixed
    marker_y=2.5,       # fixed
    title="Right Curve (Shifted Demand, Marker Fixed)"
)

# ------------------------------------------------------------------------------
# 5) Put them side by side in two columns
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_left, 
        use_container_width=False, 
        config={"staticPlot": True}, 
        key="demand_curve_left"
    )

with col2:
    st.plotly_chart(
        fig_right, 
        use_container_width=False, 
        config={"staticPlot": True}, 
        key="demand_curve_right"
    )

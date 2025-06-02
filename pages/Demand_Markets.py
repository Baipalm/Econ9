import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1) Wide layout
st.set_page_config(page_title="Interactive Demand Curves", layout="wide")
st.title("Side-by-Side Demand Curves with Movable Left Marker")

# ------------------------------------------------------------------------------
# 2) Slider: controls the left‐hand point (x_left) and thereby ΔP for the right panel
x_left = st.slider(
    label="Move Left Circle (Quantity)", 
    min_value=0.0, 
    max_value=5.0, 
    value=2.5, 
    step=0.1
)
# Price on the original demand curve P = -Q + 5:
y_left = -x_left + 5

# Compute vertical shift ΔP relative to the "old equilibrium" price 2.5:
delta_p = y_left - 2.5
# In other words, if y_left = 3.0, then ΔP = 0.5 → shift the right curve up by 0.5.

# ------------------------------------------------------------------------------
# 3) Base demand curve (no shift) for plotting left and for reference on right:
x_vals = np.linspace(0, 5, 100)
y_vals = -x_vals + 5  # Original: P = -Q + 5

def create_left_figure(marker_x: float, marker_y: float):
    """Plots P = –Q + 5 with a red dot at (marker_x, marker_y)."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines",
            fill="tozeroy",
            line=dict(color="crimson"),
            name="Demand: P = -Q + 5"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[marker_x],
            y=[marker_y],
            mode="markers",
            marker=dict(color="red", size=12),
            showlegend=False
        )
    )
    fig.update_layout(
        title="Left Curve (Movable Marker)",
        xaxis=dict(title="Quantity Demanded", range=[0, 5], fixedrange=True),
        yaxis=dict(title="Price", range=[0, 5], fixedrange=True),
        width=400,
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    return fig

def create_right_figure(vert_shift: float):
    """
    Plots a vertically shifted demand curve: P = –Q + (5 + vert_shift),
    and places a red dot at (2.5, 2.5 + vert_shift).
    """
    intercept = 5.0 + vert_shift
    y_vals_shifted = -x_vals + intercept

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals_shifted,
            mode="lines",
            fill="tozeroy",
            line=dict(color="crimson"),
            name=f"Demand (shifted by {vert_shift:+.2f})"
        )
    )
    # Place the red dot at Q=2.5, P=2.5 + vert_shift:
    x_right = 2.5
    y_right = 2.5 + vert_shift
    fig.add_trace(
        go.Scatter(
            x=[x_right],
            y=[y_right],
            mode="markers",
            marker=dict(color="red", size=12),
            showlegend=False
        )
    )
    fig.update_layout(
        title="Right Curve (Shifted Up with Demand)",
        xaxis=dict(title="Quantity Demanded", range=[0, 5], fixedrange=True),
        yaxis=dict(title="Price", range=[0, 5], fixedrange=True),
        width=400,
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    return fig

# ------------------------------------------------------------------------------
# 4) Build each figure:

# LEFT: P = -Q + 5, red dot at (x_left, y_left)
fig_left = create_left_figure(marker_x=x_left, marker_y=y_left)

# RIGHT: P = -Q + (5 + delta_p), red dot at (2.5, 2.5 + delta_p)
fig_right = create_right_figure(vert_shift=delta_p)

# ------------------------------------------------------------------------------
# 5) Display side by side
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

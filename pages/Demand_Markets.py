import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1) Wide layout
st.set_page_config(page_title="Interactive Demand Curves", layout="wide")

st.title("Side-by-Side Demand Curves with Movable Left Marker")

# ------------------------------------------------------------------------------
# 2) Slider: controls the left‐hand point (and also gives Δ for the right‐hand point).
x_left = st.slider(
    label="Move Left Circle (Quantity)", 
    min_value=0.0, 
    max_value=5.0, 
    value=2.5, 
    step=0.1
)
# The corresponding price on the original demand curve P = -Q + 5:
y_left = -x_left + 5

# Compute horizontal “shift” Δ relative to the center Q = 2.5
delta = x_left - 2.5

# ------------------------------------------------------------------------------
# 3) Helper that plots the demand curve P = -Q + 5 plus a red dot at (marker_x, marker_y).
x_vals = np.linspace(0, 5, 100)
y_vals = -x_vals + 5  # Original demand curve (no shift)

def create_demand_figure(marker_x: float, marker_y: float, title: str):
    fig = go.Figure()

    # 3a) Plot the original demand line, filled under the curve:
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
# 4) Build the two figures:

# LEFT: marker moves along P = -Q + 5 at (x_left, y_left)
fig_left = create_demand_figure(
    marker_x=x_left,
    marker_y=y_left,
    title="Left Curve (Movable Marker on P = -Q + 5)"
)

# RIGHT: demand curve stays P = -Q + 5, but the red dot sits at Q=2.5 and 
#         its price is y_right = 2.5 + Δ, so it “lies on” the shifted curve.
x_right = 2.5
y_right = 2.5 + delta

fig_right = create_demand_figure(
    marker_x=x_right,
    marker_y=y_right,
    title="Right Curve (Fixed Demand, Marker Shifts Up)"
)

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

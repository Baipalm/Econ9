import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1) Wide layout
st.set_page_config(page_title="Interactive Demand Curves", layout="wide")
st.title("Side-by-Side Demand Curves with Movable Left Marker")

# ------------------------------------------------------------------------------
# 2) Slider: controls x_left (moves the left dot along P = -Q + 5)
x_left = st.slider(
    label="Move Left Circle (Quantity)", 
    min_value=0.0, 
    max_value=5.0, 
    value=2.5, 
    step=0.1
)
# Compute its price on the original demand curve: P = -Q + 5
y_left = -x_left + 5

# We want to shift the right curve by exactly the vertical difference between
# y_left and the “old equilibrium” price 2.5:
delta_p = y_left - 2.5
# (So if y_left = 3.0 at x_left = 2.0, then delta_p = 3.0 - 2.5 = +0.5, i.e. right curve shifts up 0.5.)

# ------------------------------------------------------------------------------
# 3) Base demand‐curve points for plotting
x_vals = np.linspace(0, 5, 100)
y_vals_original = -x_vals + 5    # “Original”: P = -Q + 5

# Left‐panel figure: just draw P = -Q + 5 and put a dot at (x_left, y_left)
def create_left_figure(marker_x: float, marker_y: float):
    fig = go.Figure()
    # Plot the original demand line
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals_original,
            mode="lines",
            fill="tozeroy",
            line=dict(color="crimson"),
            name="Demand: P = -Q + 5"
        )
    )
    # Plot the red dot at (marker_x, marker_y)
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

# Right‐panel figure: shift P = -Q + 5 *up* by delta_p, i.e. P = -Q + (5 + delta_p).
# Then compute the new price at Q = 2.5 on that shifted curve, and place the red dot there.
def create_right_figure(vertical_shift: float):
    """
    - vertical_shift = ΔP = ( y_left - 2.5 ).
    - New intercept = 5 + vertical_shift.
    - So shifted demand curve is:  P = -Q + (5 + vertical_shift).
    - We fix Q_marker = 2.5 →  P_marker = -2.5 + (5 + vertical_shift).
    """
    intercept_shifted = 5.0 + vertical_shift
    y_vals_shifted = -x_vals + intercept_shifted

    fig = go.Figure()
    # 1) Plot the shifted demand line
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals_shifted,
            mode="lines",
            fill="tozeroy",
            line=dict(color="crimson"),
            name=f"Demand: P = -Q + {intercept_shifted:.2f}"
        )
    )
    # 2) Place the red dot at the intersection of Q = 2.5 with this shifted line:
    x_marker = 2.5
    y_marker = -2.5 + intercept_shifted
    fig.add_trace(
        go.Scatter(
            x=[x_marker],
            y=[y_marker],
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

# LEFT: no vertical shift → P = -Q + 5; dot at (x_left, y_left)
fig_left = create_left_figure(marker_x=x_left, marker_y=y_left)

# RIGHT: vertical shift = delta_p; dot automatically computed from the shifted line at Q = 2.5
fig_right = create_right_figure(vertical_shift=delta_p)

# ------------------------------------------------------------------------------
# 5) Display them side by side
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_left,
        use_container_width=False,
        config={"staticPlot": True},
        key="demand_curve_left",
    )

with col2:
    st.plotly_chart(
        fig_right,
        use_container_width=False,
        config={"staticPlot": True},
        key="demand_curve_right",
    )

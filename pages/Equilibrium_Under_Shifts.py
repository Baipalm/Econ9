import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Title
st.title("Interactive Supply & Demand with Guaranteed On-Screen Equilibrium")

# Base intercepts
BASE_SUPPLY_INTERCEPT = 0.0   # Supply: P = Q + (0 + shift_s)
BASE_DEMAND_INTERCEPT = 10.0  # Demand: P = –Q + (10 + shift_d)

# ——————————————————————————————
# Slider 1: Supply shift (s_s)
# Range: [-2, 2]
# ——————————————————————————————
shift_supply = st.slider(
    label="Supply Shift (adds to base intercept 0)",
    min_value=-2.0,
    max_value=2.0,
    value=0.0,
    step=0.1,
    key="shift_supply"
)

# ——————————————————————————————
# Slider 2: Demand shift (s_d)
# Range: [-2, 2]
# ——————————————————————————————
shift_demand = st.slider(
    label="Demand Shift (adds to base intercept 10)",
    min_value=-2.0,
    max_value=2.0,
    value=0.0,
    step=0.1,
    key="shift_demand"
)

# Compute actual intercepts
intercept_supply = BASE_SUPPLY_INTERCEPT + shift_supply    # b_s = 0 + s_s
intercept_demand = BASE_DEMAND_INTERCEPT + shift_demand    # b_d = 10 + s_d

# Slopes
slope_supply = 1    # Supply curve: P = Q + b_s
slope_demand = -1   # Demand curve: P = -Q + b_d

# Q-range
Q = np.linspace(0, 10, 200)

# Compute P for each curve
P_supply = slope_supply * Q + intercept_supply          # P_s = Q + b_s
P_demand = slope_demand * Q + intercept_demand          # P_d = -Q + b_d

# Compute intersection analytically:
#   -Q_eq + b_d = Q_eq + b_s  => 2·Q_eq = b_d - b_s  =>  Q_eq = (b_d - b_s) / 2
intersection_Q = (intercept_demand - intercept_supply) / 2
#   P_eq = Q_eq + b_s  OR  P_eq = (b_d + b_s) / 2
intersection_P = (intercept_demand + intercept_supply) / 2

# ——————————————————————————————
# Build Plotly figure
# ——————————————————————————————
fig = go.Figure()

# Demand curve
fig.add_trace(
    go.Scatter(
        x=Q,
        y=P_demand,
        mode="lines",
        name=f"Demand: P = -Q + {intercept_demand:.1f}",
        line=dict(color="blue", width=2)
    )
)

# Supply curve
fig.add_trace(
    go.Scatter(
        x=Q,
        y=P_supply,
        mode="lines",
        name=f"Supply: P = Q + {intercept_supply:.1f}",
        line=dict(color="red", width=2)
    )
)

# Equilibrium marker
fig.add_trace(
    go.Scatter(
        x=[intersection_Q],
        y=[intersection_P],
        mode="markers+text",
        name="Equilibrium",
        marker=dict(color="green", size=10),
        text=[f"({intersection_Q:.2f}, {intersection_P:.2f})"],
        textposition="top right"
    )
)

# Update layout: enforce fixed axes [0,10], disable zoom/pan
fig.update_layout(
    xaxis=dict(
        title="Quantity (Q)",
        range=[0, 10],
        fixedrange=True,
        showgrid=True,
        gridcolor="lightgray"
    ),
    yaxis=dict(
        title="Price (P)",
        range=[0, 10],
        fixedrange=True,
        showgrid=True,
        gridcolor="lightgray"
    ),
    width=600,
    height=600,
    legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.05),
    margin=dict(l=50, r=50, t=50, b=50),
)

# Display the chart without interactive zooming
st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "staticPlot": True,
        "displayModeBar": False
    }
)

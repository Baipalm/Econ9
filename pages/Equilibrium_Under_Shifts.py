import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Title of the app
st.title("Interactive Supply & Demand with Guaranteed On-Screen Equilibrium")

# ——————————————————————————————
# Slider 1: Supply intercept (b_s)
# Range: 0 to 10
# ——————————————————————————————
intercept_supply = st.slider(
    label="Supply Intercept (P = Q + intercept_supply)",
    min_value=0.0,
    max_value=10.0,
    value=2.0,
    step=0.5,
    key="intercept_supply"
)

# ——————————————————————————————
# Slider 2: Demand intercept (b_d)
# Range: [intercept_supply, 10]
# This ensures b_d ≥ b_s so that Q_eq ≥ 0,
# and b_d + b_s ≤ 20 automatically (since both ≤10),
# so P_eq = (b_d + b_s)/2 ≤ 10.
# ——————————————————————————————
intercept_demand = st.slider(
    label="Demand Intercept (P = -Q + intercept_demand)",
    min_value=intercept_supply,
    max_value=10.0,
    value=max(8.0, intercept_supply),
    step=0.5,
    key="intercept_demand"
)

# Fixed slopes
slope_supply = 1    # Supply: P = Q + b_s
slope_demand = -1   # Demand: P = -Q + b_d

# Define Q range
Q = np.linspace(0, 10, 100)

# Compute price curves
P_supply = slope_supply * Q + intercept_supply
P_demand = slope_demand * Q + intercept_demand

# Compute equilibrium analytically:
#   -Q_eq + b_d = Q_eq + b_s  → 2·Q_eq = b_d − b_s  →  Q_eq = (b_d − b_s) / 2
#   P_eq = Q_eq + b_s  or  P_eq = (b_d + b_s)/2
intersection_Q = (intercept_demand - intercept_supply) / 2
intersection_P = (intercept_demand + intercept_supply) / 2

# ——————————————————————————————
# Build Plotly figure with fixed axes and no zoom
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

# Update layout: fixed ranges [0,10], disable zoom/pan
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

# Render the Plotly chart without interactions
st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "staticPlot": True,
        "displayModeBar": False
    }
)

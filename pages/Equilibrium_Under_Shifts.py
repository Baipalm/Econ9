import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Title of the app
st.title("Interactive Supply and Demand Shifts (Intersection Always On-Screen)")

# Slider for shifting the supply curve (intercept)
# Default set lower so that demand > supply initially
raw_supply = st.slider(
    label="Supply Intercept (P = Q + intercept_supply)",
    min_value=0.0,
    max_value=10.0,
    value=2.0,
    step=0.5,
    key="raw_supply"
)

# Slider for shifting the demand curve (intercept)
# Default set higher so that demand > supply initially
raw_demand = st.slider(
    label="Demand Intercept (P = -Q + intercept_demand)",
    min_value=0.0,
    max_value=10.0,
    value=8.0,
    step=0.5,
    key="raw_demand"
)

# Enforce intercept_demand ≥ intercept_supply to keep equilibrium Q ≥ 0
intercept_supply = raw_supply
intercept_demand = max(raw_demand, intercept_supply)

# Fixed slopes for demand and supply
slope_demand = -1  # Demand: P = -Q + intercept_demand
slope_supply = 1   # Supply: P = Q + intercept_supply

# Define the range for quantity (Q)
Q = np.linspace(0, 10, 100)

# Compute price arrays based on current intercepts
P_demand = slope_demand * Q + intercept_demand
P_supply = slope_supply * Q + intercept_supply

# Compute intersection analytically:
intersection_Q = (intercept_supply - intercept_demand) / (slope_demand - slope_supply)
intersection_P = (intercept_demand + intercept_supply) / 2  # Equivalent to -Q_int + intercept_demand

# Create Plotly figure
fig = go.Figure()

# Add Demand line
fig.add_trace(
    go.Scatter(
        x=Q,
        y=P_demand,
        mode="lines",
        name=f"Demand: P = -Q + {intercept_demand}",
        line=dict(color="blue", width=2),
    )
)

# Add Supply line
fig.add_trace(
    go.Scatter(
        x=Q,
        y=P_supply,
        mode="lines",
        name=f"Supply: P = Q + {intercept_supply}",
        line=dict(color="red", width=2),
    )
)

# Add Intersection marker
fig.add_trace(
    go.Scatter(
        x=[intersection_Q],
        y=[intersection_P],
        mode="markers+text",
        name="Equilibrium",
        marker=dict(color="green", size=10),
        text=[f"({intersection_Q:.2f}, {intersection_P:.2f})"],
        textposition="top right",
    )
)

# Update layout: fixed axis ranges, labels, grid, disable zoom
fig.update_layout(
    xaxis=dict(
        title="Quantity (Q)",
        range=[0, 10],
        fixedrange=True,            # Prevent zooming/panning on x-axis
        showgrid=True,
        gridcolor="lightgray"
    ),
    yaxis=dict(
        title="Price (P)",
        range=[0, 10],
        fixedrange=True,            # Prevent zooming/panning on y-axis
        showgrid=True,
        gridcolor="lightgray"
    ),
    width=600,
    height=600,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    margin=dict(l=50, r=50, t=50, b=50),
)

# Display the Plotly chart in Streamlit with interactions disabled
st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "staticPlot": True,       # Disable all zooming/scrolling interactions
        "displayModeBar": False   # Hide the mode bar
    }
)

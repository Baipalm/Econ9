import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ----------------------------------------
# 1) Set up wide layout and page title
st.set_page_config(page_title="Interactive Demand Curves", layout="wide")
st.title("Combined Demand Curves (with ΔQ & ΔP Display)")

# ----------------------------------------
# 2) Add a sidebar control for Substitutes vs. Complements
mode = st.sidebar.radio(
    label="Product Relationship",
    options=["Substitutes", "Complements"],
    index=0  # default to “Substitutes”
)

# ----------------------------------------
# 3) Persist slider value in session_state
if "x_left" not in st.session_state:
    st.session_state.x_left = 2.5
x_left = st.session_state.x_left

# Compute price on the original demand curve:
y_left = -x_left + 5

# ----------------------------------------
# 4) Compute vertical shift ΔP for the right curve
delta_raw = y_left - 2.5
if mode == "Substitutes":
    delta_p = delta_raw
else:  # Complements
    delta_p = -delta_raw

# ----------------------------------------
# 5) Compute ΔQ and ΔP for display
delta_q_left   = x_left - 2.5
delta_p_left   = delta_raw
delta_q_right  = 0.0          # right Q always 2.5
delta_p_right  = delta_p

col_change_left, col_change_right = st.columns(2)
with col_change_left:
    st.markdown(f"**Left ΔQ: {delta_q_left:.2f}, ΔP: {delta_p_left:.2f}**")
with col_change_right:
    st.markdown(f"**Right ΔQ: {delta_q_right:.2f}, ΔP: {delta_p_right:.2f}**")

# ----------------------------------------
# 6) Prepare x‐values & basic formulas
x_vals = np.linspace(0, 10, 100)
y_vals_original = -x_vals + 5                  # Original: P = –Q + 5
intercept_shifted = 5.0 + delta_p
y_vals_shifted  = -x_vals + intercept_shifted  # Shifted: P = –Q + (5 + ΔP)

# Compute the red‐dot positions:
# ‣ Left marker at (x_left, y_left)
x_marker_left = x_left
y_marker_left = y_left

# ‣ Right marker at Q = 2.5
x_marker_right = 2.5
y_marker_right = -2.5 + intercept_shifted

# ----------------------------------------
# 7) Build a single combined Plotly figure
fig = go.Figure()

# 7a) Add original demand curve + marker
fig.add_trace(
    go.Scatter(
        x=x_vals,
        y=y_vals_original,
        mode="lines",
        fill="tozeroy",
        line=dict(color="crimson"),
        name="Original: P = –Q + 5",
    )
)
fig.add_trace(
    go.Scatter(
        x=[x_marker_left],
        y=[y_marker_left],
        mode="markers",
        marker=dict(color="red", size=12),
        name="Left Dot (on P=–Q+5)",
    )
)

# 7b) Add shifted demand curve + marker
fig.add_trace(
    go.Scatter(
        x=x_vals,
        y=y_vals_shifted,
        mode="lines",
        fill="tozeroy",
        line=dict(color="navy"),
        name=f"Shifted: P = –Q + {intercept_shifted:.2f}",
    )
)
fig.add_trace(
    go.Scatter(
        x=[x_marker_right],
        y=[y_marker_right],
        mode="markers",
        marker=dict(color="red", size=12, symbol="diamond"),
        name="Right Dot (on Shifted Curve)",
    )
)

# 7c) Update layout to show both on one set of axes
fig.update_layout(
    title="Combined Demand Curves",
    xaxis=dict(title="Quantity Demanded", range=[0, 10], fixedrange=True),
    yaxis=dict(title="Price",              range=[0, 10], fixedrange=True),
    width=800,
    height=500,
    margin=dict(l=40, r=40, t=50, b=40),
    legend=dict(x=0.02, y=0.98),
)

# ----------------------------------------
# 8) Display the combined figure
st.plotly_chart(
    fig,
    use_container_width=False,
    config={"staticPlot": True},
    key="combined_demand_curve"
)

# ----------------------------------------
# 9) Finally, render the slider below
st.slider(
    label="Move Left Circle (Quantity)", 
    min_value=0.0, 
    max_value=5.0, 
    value=st.session_state.x_left, 
    step=0.1, 
    key="x_left"
)

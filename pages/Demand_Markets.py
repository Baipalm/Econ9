import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configure the Streamlit page to allow a wide layout
st.set_page_config(page_title="Interactive Demand Curves", layout="wide")

st.title("Side-by-Side Demand Curves with Movable Left Marker")

# Slider widget to control the x-position of the left red circle
x_left = st.slider(
    label="Move Left Circle (Quantity)", 
    min_value=0.0, 
    max_value=5.0, 
    value=2.5, 
    step=0.1
)
# Compute the corresponding y-position on the demand line y = -x + 5
y_left = -x_left + 5

# Fixed position for the right circle (center of the line)
x_right = 2.5
y_right = 2.5

# Generate x (quantity) and y (price) values for the demand line
x_vals = np.linspace(0, 5, 100)
y_vals = -x_vals + 5  # Demand: Price = -Quantity + 5

def create_demand_figure(marker_x, marker_y):
    fig = go.Figure()

    # Demand line (filled under the curve)
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

    # Red circle at the specified marker position
    fig.add_trace(
        go.Scatter(
            x=[marker_x],
            y=[marker_y],
            mode="markers",
            marker=dict(color="red", size=12),
            showlegend=False
        )
    )

    # Configure axes range and disable zoom/pan, set square dimensions
    fig.update_layout(
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

# Create two figures:
# - Left: marker controlled by the slider
# - Right: marker fixed at (2.5, 2.5)
fig_left = create_demand_figure(x_left, y_left)
fig_right = create_demand_figure(x_right, y_right)

# Place them side by side in two equal-width columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Left Curve (Movable Marker)")
    st.plotly_chart(fig_left, use_container_width=False, config={"staticPlot": True}, key="demand_curve_left")

with col2:
    st.subheader("Right Curve (Fixed Marker)")
    st.plotly_chart(fig_right, use_container_width=False, config={"staticPlot": True}, key="demand_curve_right")

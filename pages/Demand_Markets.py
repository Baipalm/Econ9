import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configure the Streamlit page to allow a wide layout
st.set_page_config(page_title="Interactive Demand Curves", layout="wide")

st.title("Side-by-Side Demand Curves with Linked Markers")

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

# For the right graph, shift the marker by a constant offset of 2.5
constant_offset = 2.5
x_right = x_left + constant_offset
y_right = -x_right + 5  # Keep it on the same demand line

# Generate x (quantity) and y (price) values for the demand line (from 0 to 5)
x_vals = np.linspace(0, 5, 100)
y_vals = -x_vals + 5  # Demand: Price = -Q + 5

def create_demand_figure(marker_x, marker_y, x_range_max, y_range_max):
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
            range=[0, x_range_max],
            fixedrange=True
        ),
        yaxis=dict(
            title="Price",
            range=[0, y_range_max],
            fixedrange=True
        ),
        width=400,
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )

    return fig

# Determine max axis range to accommodate the shifted marker (max possible x_right = 5 + 2.5 = 7.5)
axis_max = 10

# Create two figures:
# - Left: marker controlled by the slider
# - Right: marker shifted by constant_offset + slider
fig_left = create_demand_figure(x_left, y_left, x_range_max=axis_max, y_range_max=axis_max)
fig_right = create_demand_figure(x_right, y_right, x_range_max=axis_max, y_range_max=axis_max)

# Place them side by side in two equal-width columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Left Curve (Movable Marker)")
    st.plotly_chart(fig_left, use_container_width=False, config={"staticPlot": True}, key="demand_curve_left")

with col2:
    st.subheader("Right Curve (Shifted Marker)")
    st.plotly_chart(fig_right, use_container_width=False, config={"staticPlot": True}, key="demand_curve_right")

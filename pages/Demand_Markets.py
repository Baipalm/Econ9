import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configure the Streamlit page to allow a wide layout
st.set_page_config(page_title="Side-by-Side Demand Curves", layout="wide")

st.title("Side-by-Side Demand Curves with Square Dimensions")

# Generate x (quantity) and y (price) values for a downward‐sloping demand line
x = np.linspace(0, 5, 100)
y = -x + 5  # Demand: Price = -Quantity + 5

def create_demand_figure():
    fig = go.Figure(
        data=go.Scatter(
            x=x,
            y=y,
            mode="lines",
            fill="tozeroy",               # fills area down to y=0
            line=dict(color="crimson"),
            name="Demand: P = -Q + 5"
        )
    )
    # Configure axes range and disable zoom/pan, set square dimensions
    fig.update_layout(
        xaxis=dict(
            title="Quantity Demanded",
            range=[0, 5],
            fixedrange=True  # disables zoom/pan on x-axis
        ),
        yaxis=dict(
            title="Price",
            range=[0, 5],
            fixedrange=True  # disables zoom/pan on y-axis
        ),
        width=400,
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    return fig

# Create two identical demand‐curve figures
fig1 = create_demand_figure()
fig2 = create_demand_figure()

# Place them side by side in two equal-width columns
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=False, config={"staticPlot": True})

with col2:
    st.plotly_chart(fig2, use_container_width=False, config={"staticPlot": True})

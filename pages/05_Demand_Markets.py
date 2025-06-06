import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ----------------------------------------
# 1) Set up wide layout and page title
st.set_page_config(page_title="Interactive Demand Curves", layout="wide")
st.title("Side-by-Side Demand Curves ")
st.markdown('In most cases the the demand of one market can have an impact on another. Why might this happen? Can we say what effect the demand of one market has on another? this leads use to define how the markets effect each other.')
st.markdown(''' 
**Definition: Substitutes goods**  
 Complementary goods are products that decrease in value when the demand for relative products increases. [1].
''')
st.markdown(''' 
**Definition: Complementary goods**  
 Complementary goods are products that increase in value when the demand for relative products increases. [2].
''')
st.write("**Why Is it natural to define relationship this way?**")

with st.expander("Hint: Think about the difference between a shift and movement"):
    st.write(""" Since we want the change in price to be true fpor the whole market the shift in demand makes sense. Conversely some change in demand means the entire price and quantity changed which naturallhy causes the movement we see.
     """)
# ----------------------------------------
# 2) Add a sidebar control for Substitutes vs. Complements
mode = st.sidebar.radio(
    label="Product Relationship",
    options=["Substitutes", "Complements"],
    index=0  # default to “Substitutes”
)

# ----------------------------------------
# 3) Persist slider value in session_state
#    so that we can use x_left before we actually draw the slider below.
if "x_left" not in st.session_state:
    st.session_state.x_left = 2.5
x_left = st.session_state.x_left

# Compute price on the original demand curve:
y_left = -x_left + 5

# ----------------------------------------
# 4) Compute vertical shift ΔP for the right graph,
#    inverting the sign if mode == "Complements"
delta_raw = y_left - 2.5
if mode == "Substitutes":
    delta_p = delta_raw
else:  # mode == "Complements"
    delta_p = -delta_raw

# ----------------------------------------
# 5) Compute ΔQ and ΔP for the LEFT graph (relative to (2.5, 2.5))
delta_q_left = x_left - 2.5
delta_p_left = delta_raw

# Compute ΔQ and ΔP for the RIGHT graph
delta_q_right = 0.0          # Q_right always stays at 2.5
delta_p_right = delta_p      # possibly inverted if mode=="Complements"

# ----------------------------------------
# 6) Display ΔQ & ΔP in bold, side by side *above* the graphs
col_change_left, col_change_right = st.columns(2)
with col_change_left:
    st.markdown(
        f"**Left ΔQ: {delta_q_left:.2f}, ΔP: {delta_p_left:.2f}**"
    )
with col_change_right:
    st.markdown(
        f"**Right ΔQ: {delta_q_right:.2f}, ΔP: {delta_p_right:.2f}**"
    )

# ----------------------------------------
# 7) Prepare base x‐values for plotting demand curves
x_vals = np.linspace(0, 10, 100)
y_vals_original = -x_vals + 5      # Original: P = –Q + 5

# 7a) Function to create the LEFT figure:
def create_left_figure(marker_x: float, marker_y: float):
    fig = go.Figure()
    # Original demand line (no shift)
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals_original,
            mode="lines",
            fill="tozeroy",
            line=dict(color="crimson"),
            name="Demand: P = –Q + 5"
        )
    )
    # Red dot sliding along P = –Q + 5
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
        xaxis=dict(title="Quantity Demanded", range=[0, 10], fixedrange=True),
        yaxis=dict(title="Price",           range=[0, 10], fixedrange=True),
        width=400,
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    return fig

# 7b) Function to create the RIGHT figure, shifted vertically by vertical_shift:
def create_right_figure(vertical_shift: float):
    """
    Shifted demand curve:  P = –Q + (5 + vertical_shift).
    Place red dot at Q = 2.5, so:
        P_dot = –2.5 + (5 + vertical_shift).
    """
    intercept_shifted = 5.0 + vertical_shift
    y_vals_shifted = -x_vals + intercept_shifted

    fig = go.Figure()
    # Plot the shifted line
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals_shifted,
            mode="lines",
            fill="tozeroy",
            line=dict(color="crimson"),
            name=f"Demand: P = –Q + {intercept_shifted:.2f}"
        )
    )
    # Red dot at (2.5, –2.5 + intercept_shifted)
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
        title="Right Curve (Shifted Vertically)",
        xaxis=dict(title="Quantity Demanded", range=[0, 10], fixedrange=True),
        yaxis=dict(title="Price",           range=[0, 10], fixedrange=True),
        width=400,
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    return fig

# ----------------------------------------
# 8) Build each figure

fig_left  = create_left_figure(marker_x=x_left, marker_y=y_left)
fig_right = create_right_figure(vertical_shift=delta_p)

# ----------------------------------------
# 9) Display the two graphs, side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("Left Demand Curve")
    st.plotly_chart(
        fig_left,
        use_container_width=False,
        config={"staticPlot": True},
        key="demand_curve_left"
    )

with col2:
    st.subheader("Right Demand Curve")
    st.plotly_chart(
        fig_right,
        use_container_width=False,
        config={"staticPlot": True},
        key="demand_curve_right"
    )

# ----------------------------------------
# 10) Finally, render the slider **below** the graphs
st.slider(
    label="Move Left Circle (Quantity)", 
    min_value=0.0, 
    max_value=5.0, 
    value=st.session_state.x_left, 
    step=0.1, 
    key="x_left"
)

st.markdown("""
### References

1. Hayes, Adam. “How Substitutes Work.” Investopedia, 31 July 2024, www.investopedia.com/terms/s/substitute.asp.
2. “Guide to Complementary Goods: Definition and Examples.” Indeed Career Guide, 2024, www.indeed.com/career-advice/career-development/complementary-goods.
""")



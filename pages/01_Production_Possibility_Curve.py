import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── Constants for slider maximums ────────────────────────────────────────────
MAX_L   = 40
MAX_e_x = 20
MAX_e_y = 20

# Precompute the “global” axis intercepts (when L=MAX_L, e_x=MAX_e_x, e_y=MAX_e_y)
GLOBAL_x_max = MAX_e_x * np.sqrt(MAX_L)   # ≈ 20 * √40
GLOBAL_y_max = MAX_e_y * np.sqrt(MAX_L)   # ≈ 20 * √40

@st.cache_data
def generate_curve(e_x: int, e_y: int, L: int, num_curve_pts: int = 500):
    """
    Returns:
      - x_curve, y_curve: NumPy arrays of length (num_curve_pts+2),
        with endpoints (0, y_max) and (x_max, 0) included,
      - x_max, y_max: the axis intercepts, where x_max = e_x * √L, y_max = e_y * √L.
    """
    x_max = e_x * np.sqrt(L)
    y_max = e_y * np.sqrt(L)

    # Dense points on [0, x_max]
    x_dense = np.linspace(0.0, x_max, num_curve_pts)
    inside = L - (x_dense / e_x) ** 2
    inside[inside < 0] = 0.0
    y_dense = e_y * np.sqrt(inside)

    # Prepend/append to hit the axes exactly
    x_curve = np.concatenate(([0.0], x_dense, [x_max]))
    y_curve = np.concatenate(([y_max], y_dense, [0.0]))

    return x_curve, y_curve, x_max, y_max

def compute_ppf_y(x: float, e_x: int, e_y: int, L: int) -> float:
    """
    Compute y = e_y * sqrt(L - (x/e_x)^2) for one x.
    If inside-sqrt < 0, return 0.
    """
    inside = L - (x / e_x) ** 2
    return float(e_y * np.sqrt(max(inside, 0.0)))
# ─── Title ───────────────────────────────────────────────────────────────────
st.title("Opportunity Cost along the PPF curve")

# ─── Session State for sliders ────────────────────────────────────────────────
if 'L' not in st.session_state:
    st.session_state.L = 20
if 'e_x' not in st.session_state:
    st.session_state.e_x = 10
if 'e_y' not in st.session_state:
    st.session_state.e_y = 10

L   = st.session_state.L
e_x = st.session_state.e_x
e_y = st.session_state.e_y

# Generate current curve
x_curve, y_curve, x_max, y_max = generate_curve(e_x, e_y, L)


fig_right = go.Figure()

fig_right.add_trace(
    go.Scatter(
        x=x_curve,
        y=y_curve,
        mode='lines',
        line=dict(color='royalblue', width=2,fill='tozeroy'),
        name='PPF Curve'
    )
)


fig_right.update_layout(
    uirevision='keep',
    xaxis=dict(
        range=[0, GLOBAL_x_max * 1.02],
        showgrid=False,
        title_text="Units of 🐸",
    ),
    yaxis=dict(
        range=[0, GLOBAL_y_max * 1.02],
        showgrid=False,
        title_text="Units of 🟠",
    )
)
# Disable zooming/scrolling by fixing both axes
fig_right.update_xaxes(fixedrange=True)
fig_right.update_yaxes(fixedrange=True)

# Render as a static plot (no zooming, panning, or scrolling)
st.plotly_chart(
    fig_right,
    use_container_width=False,
    config={'staticPlot': True}
)

st.markdown("---")

st.sidebar.slider("Total Labour (L)", 1, MAX_L, value=L, step=1, key="L")


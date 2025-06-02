```python
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
        where x_max = e_x * √L, y_max = e_y * √L.
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

def compute_tangent_slope(x_pt: float, e_x: int, e_y: int, L: int) -> float:
    """
    Derivative dy/dx of y = e_y * sqrt(L - (x/e_x)^2) at x = x_pt.
    dy/dx = - e_y * x / (e_x^2 * sqrt(L - (x/e_x)^2)), if inside > 0; else slope=0.
    """
    inside = L - (x_pt / e_x) ** 2
    if inside <= 0:
        return 0.0
    return - (e_y * x_pt) / (e_x**2 * np.sqrt(inside))

# ─── Title ───────────────────────────────────────────────────────────────────
st.title("Moving Point + Centered Tangent Line")

# ─── Session State for sliders ────────────────────────────────────────────────
if 'L' not in st.session_state:
    st.session_state.L = 20
if 'e_x' not in st.session_state:
    st.session_state.e_x = 10
if 'e_y' not in st.session_state:
    st.session_state.e_y = 10
if 'x_move' not in st.session_state:
    # initialize x_move at half‐curve
    st.session_state.x_move = 0.5 * (st.session_state.e_x * np.sqrt(st.session_state.L))

L   = st.session_state.L
e_x = st.session_state.e_x
e_y = st.session_state.e_y

# Generate current curve
x_curve, y_curve, x_max, y_max = generate_curve(e_x, e_y, L)

# Clamp x_move if needed
if st.session_state.x_move > x_max:
    st.session_state.x_move = float(x_max)
x_move = float(st.session_state.x_move)

# Compute moving point’s y + slope
y_move       = compute_ppf_y(x_move, e_x, e_y, L)
slope_at_move = compute_tangent_slope(x_move, e_x, e_y, L)

# ─── Build Tangent‐Line Segment Centered at (x_move, y_move) ────────────────
# We pick a fixed half‐span Δ so that the tangent line is drawn from
# (x_move − Δ) to (x_move + Δ).  Here we choose Δ = 20% of GLOBAL_x_max.
Δ = 0.20 * GLOBAL_x_max
x_tan = np.linspace(x_move - Δ, x_move + Δ, 200)
y_tan = slope_at_move * (x_tan - x_move) + y_move

# ─── Right Figure: PPF Curve, Moving Point & Centered Tangent ──────────────
fig_right = go.Figure()

fig_right.add_trace(
    go.Scatter(
        x=x_curve,
        y=y_curve,
        mode='lines',
        line=dict(color='royalblue', width=2),
        name='PPF Curve'
    )
)
fig_right.add_trace(
    go.Scatter(
        x=[x_move],
        y=[y_move],
        mode='markers',
        marker=dict(color='red', size=12, symbol='circle'),
        name='Moving Point'
    )
)
fig_right.add_trace(
    go.Scatter(
        x=x_tan,
        y=y_tan,
        mode='lines',
        line=dict(color='darkorange', width=2, dash='dash'),
        name='Centered Tangent'
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
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    width=700,
    height=500,
    margin=dict(l=20, r=20, t=20, b=20),
    annotations=[
        dict(
            x=0.95, y=0.95,
            xref='paper', yref='paper',
            text=f"Opportunity cost: {abs(slope_at_move):.2f}",
            showarrow=False,
            font=dict(size=18, color="darkorange")
        )
    ]
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

# ─── Sliders for L, e_x, e_y, and x_move (at the bottom) ────────────────────
col1, col2 = st.columns(2)
with col1:
    st.slider("Total Labour (L)", 1, MAX_L, value=L, step=1, key="L")
    st.slider("Efficiency 🐸 (e_x)", 1, MAX_e_x, value=e_x, step=1, key="e_x")
with col2:
    st.slider("Efficiency 🟠 (e_y)", 1, MAX_e_y, value=e_y, step=1, key="e_y")
    st.slider(
        "Move a point along the frontier (🐸 axis)",
        min_value=0.0,
        max_value=float(x_max),
        value=x_move,
        step=0.05,
        key="x_move"
    )
```

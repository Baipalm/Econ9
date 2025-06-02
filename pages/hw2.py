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
        with endpoints (0, y_max) and (x_max, 0) included, where
        x_max = e_x * √L, y_max = e_y * √L.
    """
    x_max = e_x * np.sqrt(L)
    y_max = e_y * np.sqrt(L)

    # Dense points on [0, x_max]
    x_dense = np.linspace(0.0, x_max, num_curve_pts)
    inside = L - (x_dense / e_x) ** 2
    inside[inside < 0] = 0
    y_dense = e_y * np.sqrt(inside)

    # Prepend/app​end to hit the axes exactly
    x_curve = np.concatenate(([0.0], x_dense, [x_max]))
    y_curve = np.concatenate(([y_max], y_dense, [0.0]))

    return x_curve, y_curve, x_max, y_max

@st.cache_data
def generate_random_points_global(num_points: int = 30, seed: int = 42):
    """
    Generates `num_points` uniformly in [0, GLOBAL_x_max] × [0, GLOBAL_y_max].
    Returns:
      - x_rand, y_rand: arrays of shape (num_points,)
    """
    np.random.seed(seed)
    x_rand = np.random.uniform(0.0, GLOBAL_x_max, num_points)
    y_rand = np.random.uniform(0.0, GLOBAL_y_max, num_points)
    return x_rand, y_rand

def compute_ppf_y(x: float, e_x: int, e_y: int, L: int) -> float:
    """
    Compute y = e_y * sqrt(L - (x/e_x)^2) for one x.
    If inside‐sqrt < 0, return 0.
    """
    inside = L - (x / e_x) ** 2
    return float(e_y * np.sqrt(max(inside, 0.0)))

# ─── Sidebar controls ─────────────────────────────────────────────────────────
st.title("Fixed‐Axis PPF with Highlighted Points")
st.sidebar.header("Settings")

L   = st.sidebar.slider("Total Labour (L)",        1, MAX_L,   20, step=1)
e_x = st.sidebar.slider("Efficiency 🐸 (e_x)",      1, MAX_e_x, 10, step=1)
e_y = st.sidebar.slider("Efficiency 🟠 (e_y)",      1, MAX_e_y, 10, step=1)

# ─── Generate (cached) PPF curve for current sliders ────────────────────────
x_curve, y_curve, x_max, y_max = generate_curve(e_x, e_y, L)

# ─── Generate (cached) random points over the GLOBAL rectangle ─────────────
x_rand, y_rand = generate_random_points_global(num_points=30)

# Determine whether each random point is “inside” (below or on) the current PPF
ppf_thresholds = e_y * np.sqrt(np.maximum(0.0, L - (x_rand / e_x) ** 2))
is_inside = (y_rand <= ppf_thresholds)

# Split into two groups:
x_inside  = x_rand[is_inside]
y_inside  = y_rand[is_inside]
x_outside = x_rand[~is_inside]
y_outside = y_rand[~is_inside]

# ─── “Moving” point on the frontier via slider ───────────────────────────────
x_move = st.slider(
    "Move a point along the frontier (🐸 axis)",
    min_value=0.0,
    max_value=float(x_max),
    value=float(x_max / 2),
    step=0.05
)
y_move = compute_ppf_y(x_move, e_x, e_y, L)

# ─── Build the Plotly figure ────────────────────────────────────────────────
fig = go.Figure()

# 1) PPF curve (filled to zero)
fig.add_trace(
    go.Scatter(
        x=x_curve,
        y=y_curve,
        mode='lines',
        fill='tozeroy',
        line=dict(color='royalblue', width=2),
        name='PPF Curve'
    )
)

# 2a) Points outside the frontier: white markers with black border
fig.add_trace(
    go.Scatter(
        x=x_outside,
        y=y_outside,
        mode='markers',
        marker=dict(
            color='white',
            size=9,
            line=dict(color='black', width=1)
        ),
        name='Outside Points'
    )
)

# 2b) Points inside or on the frontier: yellow markers with black border
fig.add_trace(
    go.Scatter(
        x=x_inside,
        y=y_inside,
        mode='markers',
        marker=dict(
            color='yellow',
            size=9,
            line=dict(color='black', width=1)
        ),
        name='Inside Points'
    )
)

# 3) The “moving” red point on the current frontier
fig.add_trace(
    go.Scatter(
        x=[x_move],
        y=[y_move],
        mode='markers',
        marker=dict(color='red', size=12, symbol='circle'),
        name='Moving Point'
    )
)

# ─── Layout tweaks ──────────────────────────────────────────────────────────
fig.update_layout(
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
    width=600,
    height=600,
)

fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True)

# ─── Render the chart ───────────────────────────────────────────────────────
st.plotly_chart(fig, use_container_width=True)

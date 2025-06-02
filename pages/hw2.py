import streamlit as st
import numpy as np
import plotly.graph_objects as go

@st.cache_data
def generate_curve_and_samples(
    e_x: int,
    e_y: int,
    L: int,
    num_curve_pts: int = 500
):
    """
    Returns:
      - x_curve, y_curve: NumPy arrays of length (num_curve_pts + 2), 
        including (0, y_max) and (x_max, 0).
      - x_max, y_max: axis‐intercepts of the PPF.
    Cached until e_x, e_y, or L change.
    """
    x_max = e_x * np.sqrt(L)
    y_max = e_y * np.sqrt(L)

    x_dense = np.linspace(0.0, x_max, num_curve_pts)
    inside = L - (x_dense / e_x) ** 2
    inside[inside < 0] = 0
    y_dense = e_y * np.sqrt(inside)

    x_curve = np.concatenate(([0.0], x_dense, [x_max]))
    y_curve = np.concatenate(([y_max], y_dense, [0.0]))

    return x_curve, y_curve, x_max, y_max

@st.cache_data
def generate_random_test_points(
    e_x: int,
    e_y: int,
    L: int,
    num_points: int = 30,
    seed: int = 42
):
    """
    Generates `num_points` uniformly in [0, x_max] × [0, y_max].
    Returns:
      - x_rand, y_rand: arrays of shape (num_points,)
    """
    np.random.seed(seed)
    x_max = e_x * np.sqrt(L)
    y_max = e_y * np.sqrt(L)

    x_rand = np.random.uniform(0.0, x_max, num_points)
    y_rand = np.random.uniform(0.0, y_max, num_points)
    return x_rand, y_rand

def compute_y_single(x: float, e_x: int, e_y: int, L: int) -> float:
    """
    Compute y = e_y * sqrt(L - (x/e_x)^2) for a single x.
    Returns 0 if inside‐sqrt is negative.
    """
    inside = L - (x / e_x)**2
    return float(e_y * np.sqrt(max(inside, 0.0)))

# ─── Sidebar controls ─────────────────────────────────────────────────────────
st.title("PPF with Transparent Background & Test Points")
st.sidebar.header("Settings")

L   = st.sidebar.slider("Total Labour (L)",        1, 40, 20, step=1)
e_x = st.sidebar.slider("Efficiency 🐸 (e_x)",      1, 20, 10, step=1)
e_y = st.sidebar.slider("Efficiency 🟠 (e_y)",      1, 20, 10, step=1)

# ─── Get (cached) PPF curve + intercepts ────────────────────────────────────
x_curve, y_curve, x_max, y_max = generate_curve_and_samples(e_x, e_y, L)

# ─── Get (cached) random test points ────────────────────────────────────────
x_rand, y_rand = generate_random_test_points(e_x, e_y, L, num_points=30)

# ─── Determine if points are inside/outside (optional) ─────────────────────
inside_threshold = e_y * np.sqrt(np.maximum(0.0, L - (x_rand / e_x) ** 2))
is_inside = (y_rand <= inside_threshold)

# ─── “Moving” point via slider ──────────────────────────────────────────────
x_move = st.slider(
    "Move a point along the frontier (🌸)",
    min_value=0.0,
    max_value=float(x_max),
    value=float(x_max / 2),
    step=0.05
)
y_move = compute_y_single(x_move, e_x, e_y, L)

# ─── Build Plotly figure ────────────────────────────────────────────────────
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

# 2) Random test points in white with black border
fig.add_trace(
    go.Scatter(
        x=x_rand,
        y=y_rand,
        mode='markers',
        marker=dict(
            color='white',
            size=10,
            line=dict(color='black', width=1)
        ),
        name='Random Points'
    )
)

# 3) Moving red marker
fig.add_trace(
    go.Scatter(
        x=[x_move],
        y=[y_move],
        mode='markers',
        marker=dict(color='red', size=12, symbol='circle'),
        name='Moving Point'
    )
)

# ─── Layout tweaks (transparent background, no grid) ────────────────────────
fig.update_layout(
    xaxis=dict(range=[0, x_max * 1.05], showgrid=False),
    yaxis=dict(range=[0, y_max * 1.05], showgrid=False),
    xaxis_title="Units of 🐸",
    yaxis_title="Units of 🟠",
    plot_bgcolor="rgba(0,0,0,0)",   # transparent plot area
    paper_bgcolor="rgba(0,0,0,0)",  # transparent surrounding area
    width=600,
    height=600
)

fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True)

# ─── Render chart ───────────────────────────────────────────────────────────
st.plotly_chart(fig, use_container_width=True)

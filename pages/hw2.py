import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
st.title("Fixed‐Axis PPF: Shared‐Axis Subplots")

# ─── Initialize slider defaults in session_state ─────────────────────────────
if "L" not in st.session_state:
    st.session_state["L"] = 20
if "e_x" not in st.session_state:
    st.session_state["e_x"] = 10
if "e_y" not in st.session_state:
    st.session_state["e_y"] = 10

# Read current slider values from session_state
L   = st.session_state["L"]
e_x = st.session_state["e_x"]
e_y = st.session_state["e_y"]

# Generate PPF curve for current (L, e_x, e_y)
x_curve, y_curve, x_max, y_max = generate_curve(e_x, e_y, L)

# Ensure x_move is initialized and clamped to [0, x_max]
default_x_move = float(x_max / 2)
if "x_move" not in st.session_state or st.session_state["x_move"] > x_max:
    st.session_state["x_move"] = default_x_move
x_move = st.session_state["x_move"]
y_move = compute_ppf_y(x_move, e_x, e_y, L)

# Generate random points globally once
x_rand, y_rand = generate_random_points_global(num_points=30)

# Determine which random points lie inside or outside the current PPF
ppf_thresholds = e_y * np.sqrt(np.maximum(0.0, L - (x_rand / e_x) ** 2))
is_inside = (y_rand <= ppf_thresholds)
x_inside  = x_rand[is_inside]
y_inside  = y_rand[is_inside]
x_outside = x_rand[~is_inside]
y_outside = y_rand[~is_inside]

# Compute tangent line at (x_move, y_move)
slope_at_move = compute_tangent_slope(x_move, e_x, e_y, L)
x_tan = np.linspace(0.0, x_max, 200)
y_tan = slope_at_move * (x_tan - x_move) + y_move

# ─── Build a single Plotly figure with two subplots (shared y‐axis) ─────────
fig = make_subplots(
    rows=1, cols=2,
    shared_yaxes=True,
    horizontal_spacing=0.05,
    subplot_titles=("PPF & Random Points", "Moving Point + Tangent")
)

# --- Subplot 1 (row=1, col=1): PPF filled + random points --- #
# 1a) PPF curve (filled to zero)
fig.add_trace(
    go.Scatter(
        x=x_curve,
        y=y_curve,
        mode="lines",
        fill="tozeroy",
        line=dict(color="royalblue", width=2),
        showlegend=False
    ),
    row=1, col=1
)

# 1b) Outside‐frontier points
fig.add_trace(
    go.Scatter(
        x=x_outside,
        y=y_outside,
        mode="markers",
        marker=dict(color="white", size=9, line=dict(color="black", width=1)),
        name="Outside Points"
    ),
    row=1, col=1
)

# 1c) Inside‐frontier points
fig.add_trace(
    go.Scatter(
        x=x_inside,
        y=y_inside,
        mode="markers",
        marker=dict(color="yellow", size=9, line=dict(color="black", width=1)),
        name="Inside Points"
    ),
    row=1, col=1
)

# --- Subplot 2 (row=1, col=2): PPF outline + moving point + tangent --- #
# 2a) PPF curve line (no fill)
fig.add_trace(
    go.Scatter(
        x=x_curve,
        y=y_curve,
        mode="lines",
        line=dict(color="royalblue", width=2),
        showlegend=False
    ),
    row=1, col=2
)

# 2b) Moving red point
fig.add_trace(
    go.Scatter(
        x=[x_move],
        y=[y_move],
        mode="markers",
        marker=dict(color="red", size=12, symbol="circle"),
        name="Moving Point"
    ),
    row=1, col=2
)

# 2c) Tangent line
fig.add_trace(
    go.Scatter(
        x=x_tan,
        y=y_tan,
        mode="lines",
        line=dict(color="darkorange", width=2, dash="dash"),
        name="Tangent Line"
    ),
    row=1, col=2
)

# ── Update axes for both subplots ────────────────────────────────────────────
# Shared y‐axis appears on the left; hide duplicate y‐tick labels on the right
fig.update_xaxes(
    dict(
        range=[0, GLOBAL_x_max * 1.02],
        showgrid=False,
        title_text="Units of 🐸"
    ),
    row=1, col=1
)
fig.update_yaxes(
    dict(
        range=[0, GLOBAL_y_max * 1.02],
        showgrid=False,
        title_text="Units of 🟠"
    ),
    row=1, col=1
)
fig.update_xaxes(
    dict(
        range=[0, GLOBAL_x_max * 1.02],
        showgrid=False,
        title_text="Units of 🐸"
    ),
    row=1, col=2
)
fig.update_yaxes(visible=False, row=1, col=2)  # hide right y‐axis ticks

# ── Final layout tweaks ─────────────────────────────────────────────────────
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    width=1000,
    height=550,
    margin=dict(l=40, r=40, t=60, b=40)
)

# ─── Render the combined figure ──────────────────────────────────────────────
st.plotly_chart(fig, use_container_width=False)

# ─── Horizontal rule separating figure and sliders ─────────────────────────
st.markdown("---")
st.subheader("Adjust All Parameters")

# ─── Sliders (below the graph) ──────────────────────────────────────────────
# Note: Using `key=...` ties each slider directly to `st.session_state[...]`.
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.slider(
        "Total Labour (L)",
        min_value=1,
        max_value=MAX_L,
        key="L"
    )

with col2:
    st.slider(
        "Efficiency 🐸 (e_x)",
        min_value=1,
        max_value=MAX_e_x,
        key="e_x"
    )

with col3:
    st.slider(
        "Efficiency 🟠 (e_y)",
        min_value=1,
        max_value=MAX_e_y,
        key="e_y"
    )

with col4:
    st.slider(
        "Move a point along the frontier (🐸 axis)",
        min_value=0.0,
        max_value=float(x_max),
        key="x_move",
        step=0.05
    )

import streamlit as st
import numpy as np

# ── (Same helper functions as before) ────────────────────────────────────────
@st.cache_data
def generate_curve(e_x: int, e_y: int, L: int, num_curve_pts: int = 500):
    x_max = e_x * np.sqrt(L)
    y_max = e_y * np.sqrt(L)
    # ... build x_curve, y_curve, etc. ...
    return x_curve, y_curve, x_max, y_max

def compute_ppf_y(x: float, e_x: int, e_y: int, L: int) -> float:
    inside = L - (x / e_x) ** 2
    return float(e_y * np.sqrt(max(inside, 0.0)))

def compute_tangent_slope(x_pt: float, e_x: int, e_y: int, L: int) -> float:
    inside = L - (x_pt / e_x) ** 2
    if inside <= 0:
        return 0.0
    return float(- (e_y * x_pt) / (e_x**2 * np.sqrt(inside)))

# ─── Title ───────────────────────────────────────────────────────────────────
st.title("ppf")

# ─── Session State Defaults ─────────────────────────────────────────────────
if 'L' not in st.session_state:
    st.session_state.L = 20
if 'e_x' not in st.session_state:
    st.session_state.e_x = 10
if 'e_y' not in st.session_state:
    st.session_state.e_y = 10
# IMPORTANT: we must ensure this is always a Python float, not numpy.float64
if 'x_move' not in st.session_state:
    st.session_state.x_move = float( (st.session_state.e_x * np.sqrt(st.session_state.L)) / 2.0 )

# ─── Read from Session State and cast to Python types ───────────────────────
L   = int(st.session_state.L)
e_x = int(st.session_state.e_x)
e_y = int(st.session_state.e_y)

# Generate curve; note that x_max, y_max come out as numpy.float64
x_curve, y_curve, x_max_np, y_max_np = generate_curve(e_x, e_y, L)

# Immediately cast x_max and y_max to plain Python floats
x_max = float(x_max_np)
y_max = float(y_max_np)

# Clamp session_state.x_move if it exceeds the new x_max
# (and force it back to a Python float)
if float(st.session_state.x_move) > x_max:
    st.session_state.x_move = x_max

# Now read x_move again as a Python float
x_move: float = float(st.session_state.x_move)

# Compute y_move and slope as plain floats
y_move = compute_ppf_y(x_move, e_x, e_y, L)
slope_at_move = compute_tangent_slope(x_move, e_x, e_y, L)


# ─── First Graph, etc. (omitted for brevity) ──────────────────────────────────
#   … (build your Plotly figures exactly as before) …
#   Assume `fig_left` and `fig_right` are created here.


# ─── Widgets (ensure all values passed to st.slider are plain Python floats/ints) ──────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.slider(
        "Total Labour (L)",
        min_value=1,
        max_value=40,
        value=int(st.session_state.L),     # Python int
        step=1,
        key="L"
    )
    st.slider(
        "Efficiency 🐸 (e_x)",
        min_value=1,
        max_value=20,
        value=int(st.session_state.e_x),    # Python int
        step=1,
        key="e_x"
    )
with col2:
    st.slider(
        "Efficiency 🟠 (e_y)",
        min_value=1,
        max_value=20,
        value=int(st.session_state.e_y),    # Python int
        step=1,
        key="e_y"
    )
st.markdown("---")

# ─── Second Graph (omitted) ──────────────────────────────────────────────────
# ... 

# ─── Opportunity‐Cost Slider at the Very Bottom ─────────────────────────────
#           (ensure both max_value and value are Python floats)
st.slider(
    "Move a point along the frontier (🐸 axis)",
    min_value=0.0,
    max_value=x_max,               # already a Python float
    value=float(st.session_state.x_move),  # explicitly a Python float
    step=0.05,
    key="x_move"
)

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

# ─── Title ───────────────────────────────────────────────────────────────────
st.title("Production Possibility Curve")
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

st.markdown('''The Production Possibility tells us the limits of what we can produce assuming we can only produce two things frogs and oranges. 
Formally Khan academy defines the Producion possibility curve as a model used to show the tradeoffs associated with allocating resources between the production of two goods. ''')
st.write("**What do you think the points on the graph represent**")
with st.expander("Hint: If the model graphs the tradeoff of production then"):
    st.write("each point must be some production of the two resources")
# ─── Generate PPF curve and random points ────────────────────────────────────
x_curve, y_curve, x_max, y_max = generate_curve(e_x, e_y, L)

x_rand, y_rand = generate_random_points_global(num_points=30)
ppf_thresholds = e_y * np.sqrt(np.maximum(0.0, L - (x_rand / e_x) ** 2))

# Color‐coding: any point within 2 units (vertically) ⇒ red
tolerance = 2.0
is_near_curve = np.abs(y_rand - ppf_thresholds) <= tolerance
is_inside     = (y_rand < ppf_thresholds) & (~is_near_curve)
is_outside    = y_rand > ppf_thresholds

x_near    = x_rand[is_near_curve]
y_near    = y_rand[is_near_curve]
x_inside  = x_rand[is_inside]
y_inside  = y_rand[is_inside]
x_outside = x_rand[is_outside]
y_outside = y_rand[is_outside]

# ─── Left Figure: PPF + Random Points ────────────────────────────────────────
fig_left = go.Figure()

fig_left.add_trace(
    go.Scatter(
        x=x_curve,
        y=y_curve,
        mode='lines',
        fill='tozeroy',
        line=dict(color='royalblue', width=2),
        name='PPF Curve'
    )
)
fig_left.add_trace(
    go.Scatter(
        x=x_near,
        y=y_near,
        mode='markers',
        marker=dict(color='red', size=9, line=dict(color='black', width=1)),
        name=f'red'
    )
)
fig_left.add_trace(
    go.Scatter(
        x=x_inside,
        y=y_inside,
        mode='markers',
        marker=dict(color='yellow', size=9, line=dict(color='black', width=1)),
        name='yellow'
    )
)
fig_left.add_trace(
    go.Scatter(
        x=x_outside,
        y=y_outside,
        mode='markers',
        marker=dict(color='white', size=9, line=dict(color='black', width=1)),
        name='white'
    )
)

fig_left.update_layout(
    uirevision='keep',  # keep pan/zoom if user has already adjusted view
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
    dragmode=False   # Disable all drag interactions
)

# Disable zooming/scrolling by fixing both axes
fig_left.update_xaxes(fixedrange=True)
fig_left.update_yaxes(fixedrange=True)

# Render as a static plot (no zooming, panning, or scrolling)
st.plotly_chart(
    fig_left,
    use_container_width=False,
    config={'staticPlot': True}
)

st.write("**Why do you think that the graph looks like this?**")
with st.expander("Hint: Think about how it would work in real life"):
    st.markdown("""Since we have a finite about of time and resources. The resource and time we spend on producing frogs can't be used to produce oranges. This is this the fundamental problem of economics.
    It is that everything is scarce.""")

# ─── Sliders for L, e_x, e_y (at the bottom) ────────────────────────────────
# ─── Sliders in the sidebar ────────────────────────────────

st.sidebar.slider("Total Labour",    1, MAX_L,   value=L,   step=1, key="L")
st.sidebar.slider("Efficiency 🐸",   1, MAX_e_x, value=e_x, step=1, key="e_x")
st.sidebar.slider("Efficiency 🟠",   1, MAX_e_y, value=e_y, step=1, key="e_y")


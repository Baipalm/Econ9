import streamlit as st
import numpy as np
import plotly.graph_objects as go

@st.cache_data
def generate_curve_and_samples(
    e_x: int,
    e_y: int,
    L: int,
    num_curve_pts: int = 500,
    num_samples: int = 10
):
    """
    Returns:
      - x_curve, y_curve: NumPy arrays of length (num_curve_pts + 2), 
        including the endpoints (0, y_max) and (x_max, 0).
      - x_samples, y_samples: `num_samples` points strictly between 0 and x_max.
      - x_max, y_max: the axis‐intercepts of the PPF.
    These outputs are cached until any of e_x, e_y, or L change.
    """
    # 1) Compute where the frontier hits the axes:
    x_max = e_x * np.sqrt(L)
    y_max = e_y * np.sqrt(L)

    # 2) Build “dense” curve points between 0 and x_max:
    x_dense = np.linspace(0.0, x_max, num_curve_pts)
    inside = L - (x_dense / e_x) ** 2
    inside[inside < 0] = 0
    y_dense = e_y * np.sqrt(inside)

    # 3) Prepend (0, y_max) and append (x_max, 0) so the curve touches both axes:
    x_curve = np.concatenate(([0.0], x_dense, [x_max]))
    y_curve = np.concatenate(([y_max], y_dense, [0.0]))

    # 4) Generate `num_samples` interior points in x, equally spaced, strictly between 0 and x_max:
    x_samples = np.linspace(
        x_max / (num_samples + 1),
        x_max * num_samples / (num_samples + 1),
        num_samples
    )
    inside_samp = L - (x_samples / e_x) ** 2
    inside_samp[inside_samp < 0] = 0
    y_samples = e_y * np.sqrt(inside_samp)

    return x_curve, y_curve, x_samples, y_samples, x_max, y_max


def compute_y_single(x: float, e_x: int, e_y: int, L: int) -> float:
    """
    Compute y = e_y * sqrt(L - (x/e_x)^2) for a single x,
    returning 0 if inside‐sqrt is negative.
    """
    inside = L - (x / e_x)**2
    return float(e_y * np.sqrt(max(inside, 0.0)))

# ─── Sidebar controls ─────────────────────────────────────────────────────────
st.title("Production Possibility Frontier (PPF) with Caching")
st.sidebar.header("Settings")

L   = st.sidebar.slider("Total Labour (L)",        1, 40, 20, step=1)
e_x = st.sidebar.slider("Efficiency 🐸 (e_x)",      1, 20, 10, step=1)
e_y = st.sidebar.slider("Efficiency 🟠 (e_y)",      1, 20, 10, step=1)

# ─── Generate (and cache) curve + samples ────────────────────────────────────
x_curve, y_curve, x_samples, y_samples, x_max, y_max = generate_curve_and_samples(e_x, e_y, L)

# ─── A “moving” point chosen via a slider ───────────────────────────────────
x_move = st.slider(
    "Move a point along the frontier (adjust 🐸)",
    min_value=0.0,
    max_value=float(x_max),
    value=float(x_max / 2),
    step=0.05
)
y_move = compute_y_single(x_move, e_x, e_y, L)

# ─── Build the Plotly figure ────────────────────────────────────────────────
fig = go.Figure()

# 1) PPF curve, filled down to zero
fig.add_trace(
    go.Scatter(
        x=x_curve,
        y=y_curve,
        mode='lines',
        fill='tozeroy',
        line=dict(color='royalblue'),
        name='PPC Curve'
    )
)

# 2) Scatter the interior data points (black dots)
fig.add_trace(
    go.Scatter(
        x=x_samples,
        y=y_samples,
        mode='markers',
        marker=dict(color='black', size=8),
        name='Sampled Data Points'
    )
)

# 3) The “moving” red point
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
    xaxis=dict(range=[0, x_max * 1.05]),
    yaxis=dict(range=[0, y_max * 1.05]),
    xaxis_title="Units of 🐸",
    yaxis_title="Units of 🟠",
    width=600,
    height=600
)
fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True)

# ─── Render the chart ───────────────────────────────────────────────────────
st.plotly_chart(fig, use_container_width=True)

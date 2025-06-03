import streamlit as st
import numpy as np
import plotly.graph_objects as go

MAX_R   = 40
MAX_e_x = 20
MAX_e_y = 20

GLOBAL_x_max = MAX_e_x * np.sqrt(MAX_R)   
GLOBAL_y_max = MAX_e_y * np.sqrt(MAX_R)  

@st.cache_data
def generate_curve(e_x: int, e_y: int, R: int, num_curve_pts: int = 500):
    
    x_max = e_x * np.sqrt(R)
    y_max = e_y * np.sqrt(R)

    # Dense points on [0, x_max]
    x_dense = np.linspace(0.0, x_max, num_curve_pts)
    inside = R - (x_dense / e_x) ** 2
    inside[inside < 0] = 0.0
    y_dense = e_y * np.sqrt(inside)

    # Prepend/append to hit the axes exactly
    x_curve = np.concatenate(([0.0], x_dense, [x_max]))
    y_curve = np.concatenate(([y_max], y_dense, [0.0]))

    return x_curve, y_curve, x_max, y_max

def compute_ppf_y(x: float, e_x: int, e_y: int, R: int) -> float:
    
    inside = R - (x / e_x) ** 2
    return float(e_y * np.sqrt(max(inside, 0.0)))
# ─── Title ───────────────────────────────────────────────────────────────────
st.title("Production Possibility Curve")
# Definition
st.markdown(''' 
**Definition: Production Possibility Curve (PPC)**  
_Production Possibility Curve_ is a representation of the possibility of production of two commodities given some fixed resource _R_ [1].
''')
# Question 1
st.write("**Why is the PPC shaped like this?**")

with st.expander("**Hint**: What does increasing production of oranges mean for the production of frogs"):
    st.write(""" Since the resource we have is finite, producing more oranges means we have to
    give up the ability to produce the more frogs. This idea that we must make choices between
    frogs and oranges is central to economics!
     """)
    
st.write("**Play around with the amount of resource available, what does the area inside and outside the curve mean?**")

with st.expander("**Hint**: Look at the definition of what the line represents"):
    st.write(" The area inside the curve represent possible productions of frogs and oranges while the area outside the curve represents productions which are impossible. We will explore more about this next page. Continue down for now.")
# ─── Session State for sliders ────────────────────────────────────────────────
if 'R' not in st.session_state:
    st.session_state.R = 20
if 'e_x' not in st.session_state:
    st.session_state.e_x = 10
if 'e_y' not in st.session_state:
    st.session_state.e_y = 10

R   = st.session_state.R
e_x = st.session_state.e_x
e_y = st.session_state.e_y

# Generate current curve
x_curve, y_curve, x_max, y_max = generate_curve(e_x, e_y, R)


fig_right = go.Figure()

fig_right.add_trace(
    go.Scatter(
        x=x_curve,
        y=y_curve,
        mode='lines',
        fill='tozeroy',
        line=dict(color='royalblue', width=2),
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

st.sidebar.slider("Resource", 1, MAX_R, value=R, step=1, key="R")

st.markdown(''' 
**Definition: Economics**  
_Economics_ is the study of how society manages it's _scarce_ resources [2].
''')
st.write("**What is meant by scarce?  How is this shown in the graph above? **")
with st.expander("**Hint**: When do you have enough resources? "):
    st.markdown("""_scarcity_ refers to the limitations on the amount of goods and services we can produce [3]. This is shown in the line of the production possibility curve. 
        The maximum amount of something that can be produced""")



st.markdown("#### References")
st.markdown("""
### References

1. The. “Production Possibility Frontier.” The Economic Times, 2025, economictimes.indiatimes.com/definition/production-possibility-frontier?from=mdr.
2. Mankiw, Nicholas. “Hill – Mankiw 9th Edn Chapter 1: Ten Principles of Economics | World Economics Association.” Www.worldeconomicsassociation.org, www.worldeconomicsassociation.org/commentaries/hill-mankiw9ed-ch1/.
3. “Scarcity.” Econlib, www.econlib.org/library/Topics/College/scarcity.html.
""")

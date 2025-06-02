import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title of the app
st.title("Interactive Supply and Demand Shifts")

# Retrieve slider values from session_state (or use defaults if not set)
intercept_demand = st.session_state.get("intercept_demand", 5)
intercept_supply = st.session_state.get("intercept_supply", 5)

# Fixed slopes for demand and supply
slope_demand = -1  # Demand: P = -Q + intercept_demand
slope_supply = 1   # Supply: P = Q + intercept_supply

# Define the range for quantity (Q)
Q = np.linspace(0, 10, 100)

# Compute price arrays based on current intercepts
P_demand = slope_demand * Q + intercept_demand
P_supply = slope_supply * Q + intercept_supply

# Compute intersection analytically:
# Solve slope_demand * Q_int + intercept_demand = slope_supply * Q_int + intercept_supply
intersection_Q = (intercept_supply - intercept_demand) / (slope_demand - slope_supply)
intersection_P = slope_demand * intersection_Q + intercept_demand

# Create the figure and axis
fig, ax = plt.subplots(figsize=(6, 6))

# Plot demand and supply lines
ax.plot(Q, P_demand, label=f"Demand: P = -Q + {intercept_demand}", color="blue", linewidth=2)
ax.plot(Q, P_supply, label=f"Supply: P = Q + {intercept_supply}", color="red", linewidth=2)

# Plot intersection marker
ax.plot(intersection_Q, intersection_P, marker="o", color="green", markersize=8, label="Equilibrium")

# Annotate the intersection point
ax.annotate(
    f"({intersection_Q:.2f}, {intersection_P:.2f})",
    xy=(intersection_Q, intersection_P),
    xytext=(intersection_Q + 0.5, intersection_P + 0.5),
    arrowprops=dict(arrowstyle="->", lw=1.5),
    fontsize=10,
    color="green"
)

# Set axis limits
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Label axes
ax.set_xlabel("Quantity (Q)")
ax.set_ylabel("Price (P)")

# Add grid and legend
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

# ——————————————————————————————
# Sliders to shift demand and supply (positioned at the bottom)
# ——————————————————————————————

# Slider for shifting the demand curve (intercept)
st.slider(
    label="Shift Demand Curve (Intercept)",
    min_value=0.0,
    max_value=10.0,
    value=intercept_demand,
    step=0.5,
    key="intercept_demand"
)

# Slider for shifting the supply curve (intercept)
st.slider(
    label="Shift Supply Curve (Intercept)",
    min_value=0.0,
    max_value=10.0,
    value=intercept_supply,
    step=0.5,
    key="intercept_supply"
)


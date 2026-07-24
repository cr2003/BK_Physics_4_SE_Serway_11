"""
Simulation Problem 17, page 102
A diving stone
"""

import numpy as np
from vpython import box, canvas, color, label, rate, sphere, vector

# =====================================================================
# 1. SCENE SETUP
# =====================================================================
scene = canvas(
    title="Stone Motion: Air to Underwater Trajectory",
    width=900,
    height=600,
    center=vector(1.5, -0.5, 0),
    background=color.gray(0.15),
)

# Physical Dimensions & Parameters
h_board = 2.50  # Height of board above water (m)
d_pool = 3.00  # Pool depth (m)
v0_mag = 4.00  # Initial launch speed (m/s)
theta = np.radians(60.0)  # Launch angle
g = 9.80  # Gravitational acceleration (m/s^2)

# Environments visual objects
water_level = 0.0
bottom_level = -d_pool

# Water body representation
water = box(
    pos=vector(2.0, bottom_level / 2, 0),
    length=8.0,
    height=d_pool,
    width=2.0,
    color=color.cyan,
    opacity=0.35,
)

# Diving Board
board = box(
    pos=vector(-0.5, h_board - 0.1, 0),
    length=1.0,
    height=0.2,
    width=0.8,
    color=color.orange,
)

# Pool Bottom Line
bottom = box(
    pos=vector(2.0, bottom_level - 0.05, 0),
    length=8.0,
    height=0.1,
    width=2.0,
    color=color.white,
)

# The Stone
stone = sphere(
    pos=vector(0, h_board, 0),
    radius=0.08,
    color=color.yellow,
    make_trail=True,
    trail_type="curve",
    trail_color=color.yellow,
    retain=500,
)

# On-screen timer display
timer_label = label(
    pos=vector(-1.0, h_board + 0.8, 0),
    text="Time: 0.00 s",
    height=16,
    box=False,
    color=color.white,
)

# =====================================================================
# 2. INITIAL CONDITIONS
# =====================================================================
vx = v0_mag * np.cos(theta)
vy = v0_mag * np.sin(theta)
v = vector(vx, vy, 0)

dt = 0.002  # Time step size for numerical integration
t = 0.0
entered_water = False

# =====================================================================
# 3. ANIMATION LOOP
# =====================================================================
while stone.pos.y > bottom_level:
    rate(300)  # Controls execution speed of the visual frame

    # Check transition into water
    if not entered_water and stone.pos.y <= water_level:
        entered_water = True

        # Calculate impact speed and direction angle
        v_impact_mag = v.mag
        # Half speed upon entering water, maintain original vector direction
        v = (v / v_impact_mag) * (v_impact_mag / 2.0)

        # Change trail color underwater to visually distinguish phases
        stone.trail_color = color.magenta

    # Motion Updates
    if not entered_water:
        # Phase 1: Projectile motion under gravity
        v.y -= g * dt
    else:
        # Phase 2: Constant velocity vector underwater
        pass

    # Update position and elapsed time
    stone.pos += v * dt
    t += dt

    # Update timer UI
    timer_label.text = f"Time: {t:.2f} s"

# Final readout marker at pool bottom
label(
    # pos=stone.pos + vector(0.6, 0.3, 0),
    pos=stone.pos + vector(1, 0.3, 0),
    text=f"Impact!\nTotal Time: {t:.2f} s",
    height=14,
    color=color.green,
    box=True,
)

################### The End ###################
print("\n\nAnimation complete.")
scene.waitfor("click")

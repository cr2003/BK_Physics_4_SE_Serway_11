"""
Simulation Problem 39, page 104
Baseball Trajectory vs. Bleachers
"""

import numpy as np
from vpython import box, canvas, color, label, rate, sphere, vector

# =====================================================================
# 1. SCENE SETUP
# =====================================================================
scene = canvas(
    title="Problem 39: Baseball Trajectory vs. Bleachers",
    width=900,
    height=600,
    center=vector(65, 12, 0),
    background=color.gray(0.12),
)

# Physical Constants & Given Inputs
g = 9.80  # Gravity (m/s^2)
v0 = 41.7  # Initial launch speed (m/s)
theta = np.radians(35.0)  # Launch angle
y0 = 1.00  # Initial height (m)

x_bleachers = 130.0  # Horizontal distance to bleachers (m)
h_bleachers = 24.0  # Height of top row of bleachers (m)

# Ground
ground = box(
    pos=vector(75, -0.2, 0),
    length=160,
    height=0.4,
    width=10,
    color=color.gray(0.4),
)

# Bleachers Structure (Wall at x = 130m, height = 24m)
bleachers = box(
    pos=vector(x_bleachers + 2.0, h_bleachers / 2.0, 0),
    length=4.0,
    height=h_bleachers,
    width=6.0,
    color=color.orange,
    opacity=0.7,
)

# Target marker on top of bleachers (24.0m height)
top_marker = sphere(
    pos=vector(x_bleachers, h_bleachers, 0),
    radius=0.6,
    color=color.red,
)
label(
    pos=vector(x_bleachers, h_bleachers + 3.0, 0),
    text="Top Row (24.0 m)",
    height=14,
    box=False,
    color=color.red,
)

# Home Plate
home_plate = box(
    pos=vector(0, 0.01, 0),
    length=0.8,
    height=0.02,
    width=0.8,
    color=color.white,
)

# The Baseball
ball = sphere(
    pos=vector(0, y0, 0),
    radius=0.4,
    color=color.yellow,
    make_trail=True,
    trail_type="curve",
    trail_color=color.yellow,
    retain=1000,
)

# On-screen HUD readout
hud_label = label(
    pos=vector(20, 28, 0),
    text="Time: 0.00 s | Height: 1.00 m",
    height=16,
    box=False,
    color=color.white,
)

# =====================================================================
# 2. INITIAL VELOCITY & INTEGRATION LOOP
# =====================================================================
v = vector(v0 * np.cos(theta), v0 * np.sin(theta), 0)
dt = 0.002
t = 0.0

# Run until ball reaches x = 130 m or hits ground
while ball.pos.x < x_bleachers and ball.pos.y > 0:
    rate(250)

    # Gravity update
    v.y -= g * dt
    ball.pos += v * dt
    t += dt

    hud_label.text = f"Time: {t:.2f} s | x: {ball.pos.x:.1f} m | y: {ball.pos.y:.1f} m"

# =====================================================================
# 3. IMPACT ANALYSIS
# =====================================================================
impact_height = ball.pos.y
height_shortfall = h_bleachers - impact_height

# Visual marker for point of impact on the bleachers
sphere(pos=ball.pos, radius=0.7, color=color.magenta)

label(
    # pos=ball.pos + vector(-15, 0, 0),
    pos=ball.pos + vector(-15, 30, 0),
    text=(
        f"IMPACT AT BLEACHERS!\n"
        f"Height reached: {impact_height:.2f} m\n"
        f"Short of top by: {height_shortfall:.2f} m"
    ),
    height=14,
    color=color.cyan,
    box=True,
)

print(f"Impact height at x = 130 m: {impact_height:.2f} m")
print(f"Shortfall from 24.0 m top row: {height_shortfall:.2f} m")


################### The End ###################
print("\n\nAnimation complete.")
scene.waitfor("click")

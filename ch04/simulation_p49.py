"""
Simulation Problem 49, page 105
Ski Jump on Downward Slope
"""

import numpy as np
from vpython import box, canvas, color, label, rate, sphere, vector

# =====================================================================
# 1. PHYSICAL CONSTANTS & CALCULATIONS
# =====================================================================
g = 9.80  # Gravitational acceleration (m/s^2)
v0 = 10.0  # Launch velocity (m/s)
theta = np.radians(15.0)  # Launch angle above horizontal (rad)
phi = np.radians(50.0)  # Incline angle below horizontal (rad)

# Calculated distance along slope (d) and time of flight (t_flight)
d_land = (2 * (v0**2) * np.cos(theta) * np.sin(theta + phi)) / (g * (np.cos(phi) ** 2))
t_flight = (d_land * np.cos(phi)) / (v0 * np.cos(theta))

# =====================================================================
# 2. SCENE SETUP
# =====================================================================
scene = canvas(
    title="Problem 49: Ski Jump on Downward Slope",
    width=950,
    height=600,
    background=color.gray(0.1),
)

# Center the camera focus further right and lower down so the entire slope is visible
scene.center = vector(12, -10, 0)
scene.camera.pos = vector(12, -8, 42)

# --- VISUAL ENVIRONMENT ---
# Ramp / Launch Platform (at origin)
ramp = box(
    pos=vector(-2, 0.5, 0),
    size=vector(4, 1, 3),
    color=color.gray(0.6),
)

# Enlarged Sloped Landing Hill (extended length to 50 m)
slope_length = 50.0
slope_center = vector(
    (slope_length / 2) * np.cos(phi), -(slope_length / 2) * np.sin(phi), 0
)
slope = box(
    pos=slope_center,
    size=vector(slope_length, 0.5, 6),
    axis=vector(np.cos(phi), -np.sin(phi), 0),
    color=color.white,
    opacity=0.85,
)

# Impact Target Marker (placed exactly on the surface at d_land)
impact_pos = vector(d_land * np.cos(phi), -d_land * np.sin(phi), 0)
target = sphere(
    pos=impact_pos,
    radius=0.5,
    color=color.red,
)

# --- REPOSITIONED HUD LABELS ---
hud = label(
    pos=vector(-4, 12, 0),
    text="Time: 0.00 s\nPosition: (0.0 m, 0.0 m)",
    height=14,
    box=True,
    border=6,
    color=color.white,
    line=False,
)

label(
    # pos=vector(impact_pos.x + 4, impact_pos.y - 2, 0),
    pos=vector(impact_pos.x - 5, impact_pos.y - 2, 0),
    text=f"Landing Point\nd = {d_land:.1f} m",
    height=13,
    color=color.red,
    box=False,
)

# =====================================================================
# 3. ANIMATION LOOP
# =====================================================================
skier = sphere(
    pos=vector(0, 0, 0),
    radius=0.45,
    color=color.yellow,
    make_trail=True,
    trail_type="curve",
    trail_color=color.cyan,
    retain=1000,
)

# Initial velocity vector
v_vec = vector(v0 * np.cos(theta), v0 * np.sin(theta), 0)
dt = 0.002
t = 0.0

# Run trajectory until hitting the slope surface
while t <= t_flight:
    rate(200)

    # Kinematic integration
    v_vec.y -= g * dt
    skier.pos += v_vec * dt
    t += dt

    # Real-time HUD update
    hud.text = (
        f"Flight Time: {t:.2f} s / {t_flight:.2f} s\n"
        f"Speed: {v_vec.mag:.2f} m/s\n"
        f"Position: ({skier.pos.x:.1f} m, {skier.pos.y:.1f} m)"
    )

# Final Completion HUD Banner
label(
    pos=vector(24, 12, 0),
    text=(
        "--- LANDING COMPLETE ---\n"
        f"Slope Distance (d) : {d_land:.2f} m\n"
        f"Flight Time (t)    : {t_flight:.2f} s\n"
        f"Velocity (v_x, v_y): ({v_vec.x:.2f}, {v_vec.y:.2f}) m/s"
    ),
    height=14,
    color=color.green,
    box=True,
    border=8,
    line=False,
)

print("--- Simulation Complete ---")
print(f"Distance along slope (d): {d_land:.2f} m")
print(
    f"Velocity components at impact: v_x = {v_vec.x:.2f} m/s, v_y = {v_vec.y:.2f} m/s"
)
################### The End ###################
print("\n\nAnimation complete.")
scene.waitfor("click")

"""
Simulation Problem 41, page 104
Lunar Cannon Package Orbit
"""

import numpy as np
from vpython import box, canvas, color, cylinder, label, pi, rate, sphere, vector

# =====================================================================
# 1. SCENE & PHYSICAL SETUP
# =====================================================================
# Real physical dimensions
R_moon = 1.737e6  # Moon radius (m)
g_moon = 9.80 / 6.0  # Lunar surface gravity (m/s^2)
v_muzzle = np.sqrt(g_moon * R_moon)  # Orbital speed (~1684 m/s)
T_orbit = 2 * pi * np.sqrt(R_moon / g_moon)  # Period (~6480 s)

# Visual scale multiplier to enlarge the render
visual_scale = 2.5
scale = (1.0 / R_moon) * visual_scale

scene = canvas(
    title="Problem 41: Lunar Cannon Package Orbit",
    width=900,
    height=600,
    center=vector(0, 0, 0),
    background=color.gray(0.05),
)
# Adjusted camera distance for the enlarged Moon
scene.camera.pos = vector(0, 0, 5.0)

# =====================================================================
# 2. OBJECTS & VISUAL ELEMENTS
# =====================================================================
# Enlarge the Moon
moon = sphere(
    pos=vector(0, 0, 0),
    radius=1.0 * visual_scale,
    color=color.gray(0.7),
    # texture="https://i.imgur.com/3N4o1K9.jpg",  # Lunar surface texture
    texture="https://upload.wikimedia.org/wikipedia/commons/2/26/Solarsystemscope_texture_2k_moon.jpg",
    shininess=0,  # La superficie lunar no es reflectante
)

# Launch Cannon (at top pole)
cannon = cylinder(
    pos=vector(0, 1.0 * visual_scale, 0),
    axis=vector(0.15, 0, 0),  # Points horizontally (+x direction)
    radius=0.03,
    color=color.white,
)

# The Experiment Package
package = sphere(
    pos=vector(0, 1.002 * visual_scale, 0),
    radius=0.04,
    color=color.yellow,
    make_trail=True,
    trail_type="curve",
    trail_color=color.cyan,
    retain=2000,
)

# Start / Return Marker
start_marker = box(
    pos=vector(0, 1.02 * visual_scale, 0),
    size=vector(0.02, 0.05, 0.02),
    color=color.red,
)

# --- REPOSITIONED LABELS (Clearing the enlarged Moon) ---

# 1. Cannon Label (Placed well above the top pole)
label(
    pos=vector(0, 3, 0),
    text="Launch / Return Point",
    height=14,
    box=False,
    color=color.red,
)

# 2. HUD Readout (Top-Left corner)
hud_label = label(
    pos=vector(-5, 5, 0),
    text="Time: 0.0 min / 108.0 min\nDistance: 0 km",
    height=15,
    box=True,
    border=6,
    color=color.white,
    line=False,
)

# =====================================================================
# 3. ORBIT SIMULATION LOOP
# =====================================================================
r_vec = vector(0, R_moon, 0)
v_vec = vector(v_muzzle, 0, 0)

dt = 2.0  # Time step in seconds
t = 0.0

while t < T_orbit:
    rate(200)

    # Gravitational acceleration toward Moon center
    r_mag = r_vec.mag
    acc = -g_moon * (r_vec / r_mag)

    # Euler-Cromer Integration
    v_vec += acc * dt
    r_vec += v_vec * dt
    t += dt

    # Update visual package position with scale factor
    package.pos = r_vec * scale

    # HUD updates
    t_min = t / 60.0
    dist_km = (v_muzzle * t) / 1000.0
    hud_label.text = (
        f"Time: {t_min:.1f} min / {T_orbit / 60:.1f} min\nDistance: {dist_km:.0f} km"
    )

# 3. Completion Banner (Top-Right corner)
label(
    pos=vector(5, 5, 0),
    text=f"ORBIT COMPLETE!\nReturn Time: {t / 60:.1f} min",
    height=15,
    color=color.green,
    box=True,
    border=8,
    line=False,
)

print("--- Simulation Complete ---")
print(f"Muzzle Velocity : {v_muzzle:.2f} m/s")
print(f"Total Orbit Time: {t / 60:.2f} minutes")

################### The End ###################
print("\n\nAnimation complete.")
scene.waitfor("click")

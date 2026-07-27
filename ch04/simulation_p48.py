"""
Simulation Problem 48, page 105
pirates
"""

import numpy as np
from vpython import box, canvas, color, cylinder, label, rate, sphere, vector

# =====================================================================
# 1. PHYSICAL CONSTANTS & PROBLEM CALCULATIONS
# =====================================================================
g = 9.80  # Gravity (m/s^2)
h = 7.00  # Fort height above water (m)
d = 75.0  # Horizontal distance to ship (m)

# --- Part (a): Horizontal Launch Speed ---
t_fall_a = np.sqrt(2 * h / g)
v0_a = d / t_fall_a  # ~62.74 m/s

# --- Part (b): Half-Speed Angled Launches ---
v0_b = 0.500 * v0_a  # ~31.37 m/s

# Solving quadratic equation for tan(theta): C * u^2 - d * u + (C - h) = 0
C = (g * d**2) / (2 * v0_b**2)  # C = 4 * h = 28.0 m
a_quad = C
b_quad = -d
c_quad = C - h

discriminant = b_quad**2 - 4 * a_quad * c_quad

# Two valid launch angles
u_low = (-b_quad - np.sqrt(discriminant)) / (2 * a_quad)
u_high = (-b_quad + np.sqrt(discriminant)) / (2 * a_quad)

theta_low = np.arctan(u_low)  # ~17.62 deg
theta_high = np.arctan(u_high)  # ~67.04 deg

# =====================================================================
# 2. SCENE & ENVIRONMENT SETUP
# =====================================================================
scene = canvas(
    title="Problem 48: Pirates of the Caribbean Cannon Trajectories",
    width=950,
    height=600,
    center=vector(d / 2.0, 15, 0),
    background=color.gray(0.1),
)
scene.camera.pos = vector(d / 2.0, 20, 110)

# Ocean Water surface
water = box(
    pos=vector(d / 2.0, -0.2, 0),
    size=vector(110, 0.4, 30),
    color=color.blue,
    opacity=0.6,
)

# Fort Platform at x = 0, y = 7m
fort = box(
    pos=vector(-5, h / 2.0, 0),
    size=vector(10, h, 12),
    color=color.gray(0.5),
)
label(
    pos=vector(-5, h + 3, 0),
    text="Fort Cannon\n(Height = 7.0 m)",
    height=13,
    box=False,
    color=color.white,
)

# Pirate Ship at x = 75m, y = 0m
ship_hull = box(
    pos=vector(d, 1.5, 0),
    size=vector(12, 3.0, 6),
    color=color.orange,
)
ship_mast = cylinder(
    pos=vector(d, 3.0, 0),
    axis=vector(0, 12, 0),
    radius=0.3,
    color=color.white,
)
label(
    pos=vector(d, -3, 0),
    text="Pirate Ship\n(Distance = 75.0 m)",
    height=13,
    box=False,
    color=color.white,
)

# Top-Left HUD Readout
hud = label(
    pos=vector(-10, 38, 0),
    text="Initializing simulation...",
    height=14,
    box=True,
    color=color.white,
    line=False,
)


# =====================================================================
# 3. HELPER FUNCTION TO RUN TRAJECTORIES
# =====================================================================
def fire_cannonball(v0, theta_rad, ball_color, label_text):
    """Simulates a single cannonball trajectory until hit."""
    ball = sphere(
        pos=vector(0, h, 0),
        radius=0.8,
        color=ball_color,
        make_trail=True,
        trail_type="curve",
        trail_color=ball_color,
        retain=1000,
    )

    v = vector(v0 * np.cos(theta_rad), v0 * np.sin(theta_rad), 0)
    dt = 0.002
    t = 0.0

    while ball.pos.y > 0 and ball.pos.x < d + 1.0:
        rate(300)
        v.y -= g * dt
        ball.pos += v * dt
        t += dt

        hud.text = (
            f"Active Simulation: {label_text}\n"
            f"Speed: {v0:.1f} m/s | Angle: {np.degrees(theta_rad):.1f}°\n"
            f"Time: {t:.2f} s | Position: ({ball.pos.x:.1f} m, {ball.pos.y:.1f} m)"
        )

    # Impact marker
    sphere(pos=ball.pos, radius=1.2, color=color.red)
    return ball, t


# =====================================================================
# 4. EXECUTE ALL 3 TRAJECTORIES
# =====================================================================

# 1. Part (a): Horizontal Launch (100% Speed)
scene.waitfor("click")
ball_a, t_a = fire_cannonball(
    v0=v0_a,
    theta_rad=0.0,
    ball_color=color.yellow,
    label_text="Part (a) Horizontal Hit (v0 = 62.7 m/s, θ = 0°)",
)

# 2. Part (b): Low Angle Launch (50% Speed)
scene.waitfor("click")
ball_b1, t_b1 = fire_cannonball(
    v0=v0_b,
    theta_rad=theta_low,
    ball_color=color.cyan,
    label_text="Part (b) Low-Angle Hit (v0' = 31.4 m/s, θ = 17.6°)",
)

# 3. Part (b): High Angle Launch (50% Speed)
scene.waitfor("click")
ball_b2, t_b2 = fire_cannonball(
    v0=v0_b,
    theta_rad=theta_high,
    ball_color=color.magenta,
    label_text="Part (b) High-Angle Hit (v0' = 31.4 m/s, θ = 67.0°)",
)

# Final Summary Banner
hud.text = (
    "--- ALL TRAJECTORIES COMPLETE ---\n"
    f"Part (a) θ = 0.0°  | v = {v0_a:.1f} m/s | Flight Time: {t_a:.2f} s\n"
    f"Part (b) θ = 17.6° | v = {v0_b:.1f} m/s | Flight Time: {t_b1:.2f} s\n"
    f"Part (b) θ = 67.0° | v = {v0_b:.1f} m/s | Flight Time: {t_b2:.2f} s"
)

print("\n--- Simulation Summary ---")
print(f"Part (a) Muzzle speed required : {v0_a:.2f} m/s")
print(f"Part (b) 50% Reduced speed      : {v0_b:.2f} m/s")
print(f"Part (b) Low launch angle       : {np.degrees(theta_low):.2f}°")
print(f"Part (b) High launch angle      : {np.degrees(theta_high):.2f}°")

################### The End ###################
print("\n\nAnimation complete.")
scene.waitfor("click")

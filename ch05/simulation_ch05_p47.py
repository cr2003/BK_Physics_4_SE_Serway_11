"""
Chapter 05
Simulation Problem 47, page 140
Container Ship vs. Reef Simulation
"""

from vpython import *

# 1. Setup 3D Scene / Canvas
scene = canvas(
    title="Problem 47: Container Ship vs. Reef Simulation (High Contrast)",
    width=900,
    height=500,
    center=vector(450, 0, 0),
    background=color.cyan,
)

# 2. Physics Parameters & Constants
v0 = 2.50  # Initial velocity (m/s)
d_reef = 900.0  # Initial distance to reef (m)
F_wind = 9.00e3  # Wind force toward reef (N)
F_reverse = 1.25e5  # Reverse/drag force away from reef (N)
m = 5.50e7  # Ship mass (kg)

# Net force and acceleration
F_net = F_wind - F_reverse  # Negative, accelerating away from reef (braking)
a = F_net / m  # Deceleration (m/s^2)

# 3. Create 3D Objects
# Ocean Water Surface
water = box(
    pos=vector(450, -5, 0),
    size=vector(1200, 2, 200),
    color=vector(0, 0.4, 0.8),
    opacity=0.7,
)

# Reef (Red barrier at x = 900)
reef = box(pos=vector(d_reef + 10, 15, 0), size=vector(20, 40, 150), color=color.red)
# UPDATED: Changed label color to black
reef_label = label(
    pos=reef.pos + vector(0, 30, 0), text="REEF (900 m)", height=16, color=color.black
)

# Ship
ship = box(pos=vector(0, 10, 0), size=vector(60, 20, 30), color=color.gray(0.2))
ship_bow = cone(
    pos=vector(30, 10, 0), axis=vector(20, 0, 0), radius=15, color=color.gray(0.2)
)

# Initial Position Marker
start_marker = cylinder(
    pos=vector(0, 0, -60), axis=vector(0, 40, 0), radius=2, color=color.yellow
)
# UPDATED: Changed label color to black
label(pos=vector(0, 50, -60), text="Start (t = 0s)", height=12, color=color.black)

# Velocity & Force Vector Indicators
v_arrow = arrow(
    pos=ship.pos + vector(0, 25, 0),
    axis=vector(v0 * 20, 0, 0),
    color=color.green,
    shaftwidth=3,
)
F_arrow = arrow(
    pos=ship.pos + vector(0, 35, 0),
    axis=vector(F_net / 1000, 0, 0),
    color=color.orange,
    shaftwidth=3,
)

# Real-time Telemetry Label
# UPDATED: Changed color to black and added a contrasting background (opacity=0.4)
telemetry = label(
    pos=vector(450, 100, 0),
    text="",
    height=14,
    color=color.black,
    box=True,
    opacity=0.4,
    border=4,
)

# 4. Simulation Control Parameters
x = 0.0
v = v0
t = 0.0
dt = 0.5  # Time step (seconds)
time_scale = 20  # Simulation speedup factor

# 5. Simulation Loop
while x < d_reef and v > 0:
    rate(1 / dt * time_scale)

    # Update Physics
    v += a * dt
    x += v * dt + 0.5 * a * (dt**2)
    t += dt

    # Update 3D Positions
    ship.pos.x = x
    ship_bow.pos.x = x + 30
    v_arrow.pos.x = x
    v_arrow.axis.x = v * 20
    F_arrow.pos.x = x

    # Update Telemetry Text
    telemetry.text = (
        f"Time: {t:.1f} s\n"
        f"Position: {x:.1f} m / {d_reef:.0f} m\n"
        f"Velocity: {v:.3f} m/s\n"
        f"Deceleration: {a:.6f} m/s²"
    )

# 6. Final Status Output
if x >= d_reef:
    impact_v = v
    telemetry.text += f"\n\nCRASH DETECTED!\nImpact Velocity: {impact_v:.3f} m/s"
    reef.color = color.magenta
else:
    telemetry.text += "\n\nShip stopped safely before the reef."


################### The End ###################
print("\n\nAnimation complete.")
scene.waitfor("click")

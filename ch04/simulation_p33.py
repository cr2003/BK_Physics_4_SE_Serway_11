"""
Simulation Problem 33, page 103
Truck Projectile Motion
"""

from vpython import *
from astropy import units as u

# --- Scene Setup ---
scene = canvas(
    title="Truck Projectile Motion", width=800, height=400, background=color.gray(0.2)
)
scene.range = 15  # Adjust zoom level
scene.center = vec(8, 2, 0)  # Focused on the middle of the path

# Constants
v_truck_val = 9.50
v_can_vert_val = 8.25
g_val = 9.80
t_flight = 1.684
start_x = -5  # Start on the left side

# --- Environment (The Floor) ---
# Asphalt road
road = box(pos=vec(8, 0, 0), size=vec(40, 0.2, 4), color=vec(0.2, 0.2, 0.2))

# Road markings (White dashes)
for x in range(-10, 30, 4):
    box(pos=vector(x, 0.1, 0), size=vec(1.5, 0.05, 0.1), color=color.white)

# Objects
truck = box(pos=vector(start_x, 0.2, 0), size=vec(3, 0.8, 1.5), color=color.blue)
# The boy (represented by a cylinder)
boy = cylinder(
    pos=truck.pos + vec(0, 0.4, 0), axis=vec(0, 0.8, 0), radius=0.2, color=color.orange
)
can = sphere(
    pos=truck.pos + vec(0, 1.2, 0),
    radius=0.15,
    color=color.red,
    make_trail=True,
    trail_color=color.yellow,
)

# --- Initial Velocity
# Relative to ground: vx = truck_speed, vy=throw_speed
v_can = vec(v_truck_val, v_can_vert_val, 0)

# --- Simulation loop ---
dt = 0.001
t = 0

# Label to track coordinates
coords = label(pos=vec(8, 8, 0), text="Time: 0s", height=12)

while t < t_flight:
    rate(100)

    # Update truck and boy positions
    truck.pos.x += v_truck_val * dt
    boy.pos.x += v_truck_val * dt

    # Update can (Projectile motion)
    can.pos += v_can * dt
    v_can.y -= g_val * dt  # Gravity affects vertical velocity
    t += dt
    coords.text = f"Time: {t:.2f}s \nDistance: {truck.pos.x - start_x:.2f}m"

# Final indicator to show where it was caught
sphere(pos=can.pos, radius=0.3, color=color.green, opacity=0.5)
print(f"Distance covered: {truck.pos.x - start_x:.2f} meters")

print(f"Truck position: {truck.pos} m")
print(f"Can position: {can.pos} m")


################### The End ###################
print("\n\nAnimation complete.")
scene.waitfor("click")

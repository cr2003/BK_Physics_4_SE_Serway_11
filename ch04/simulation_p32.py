"""
Simulation Problem 32, page 103
Coast Guard Interception
"""

from vpython import *
from astropy import units as u


# --- Scene Setup ---
scene = canvas(
    title="Coast Guard Interception", width=800, height=600, center=vec(10, 20, 0)
)
ground = box(pos=vector(15, 25, -0.1), size=vec(60, 80, 0.01), color=color.gray(0.2))


# Constants & Data
def nav_to_math(bearing_deg):
    """Converts compass bearing (N=0, Clockwise) to math angle (E=0, CCW)"""
    return radians((90 - bearing_deg) % 360)


v_vessel_speed = 26.0
v_vessel_math_angle = nav_to_math(40.0)  # 40 deg E of N

v_boat_speed = 50.0
v_boat_math_angle = nav_to_math(27.7)  # The Book's Heading

# Objects
# Initial Position: 20 km at 15 deg E of N
pos_angle = nav_to_math(15.0)
vessel_start = vec(20 * cos(pos_angle), 20 * sin(pos_angle), 0)
vessel = sphere(pos=vessel_start, radius=0.8, color=color.yellow, make_trail=True)
vessel_vel = vec(
    v_vessel_speed * cos(v_vessel_math_angle),
    v_vessel_speed * sin(v_vessel_math_angle),
    0,
)

# Speedboat
boat = sphere(pos=vec(0, 0, 0), radius=0.8, color=color.red, make_trail=True)
boat_vel = vec(
    v_boat_speed * cos(v_boat_math_angle), v_boat_speed * sin(v_boat_math_angle), 0
)

# Labels
label(pos=vec(0, 0, 0), text="Radar Station", height=10, yoffset=-15)
target_label = label(pos=vessel.pos, text="Vessel", height=10, yoffset=15)

# Simulation

dt = 0.001
t = 0
while t < 2:
    rate(100)

    # Update positions
    vessel.pos += vessel_vel * dt
    boat.pos += boat_vel * dt

    # Update Label
    target_label.pos = vessel.pos

    # Check for interception
    dist = mag(vessel.pos - boat.pos)
    if dist < 0.5:
        time = t * u.h
        time = time.to(u.min)
        print(f"INTERCEPTION at t = {time:.0f}")
        print(f"Location: {vessel.pos} km")
        sphere(pos=vessel.pos, radius=1.5, color=color.orange, opacity=0.4)
        break

    t += dt


################### The End ###################
print("\n\nAnimation complete.")
scene.waitfor("click")

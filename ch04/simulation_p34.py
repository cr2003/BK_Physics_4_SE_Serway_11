"""
Simulation Problem 33, page 103
Truck Projectile Motion - Release in front of camera moving right
"""

from vpython import *

# Constants
r = 0.300
h = 1.20
v_mag = 4.041
g = 9.80

# --- Scene Setup ---
scene = canvas(
    title="Circular Motion to Projectile (Release in Front, Moving Right)",
    width=800,
    height=600,
    background=color.gray(0.1),
)
scene.camera.pos = vector(1, 0, 4)
scene.center = vec(1, -h / 2, 0)


# Ground and reference Line
ground = box(pos=vec(0, -h - 0.01, 0), size=vec(5, 0.01, 5), color=color.gray(0.3))
# The white reference line
x_axis_ref = cylinder(
    pos=vec(-1, -h, 0), axis=vec(2, 0, 0), radius=0.02, color=color.white
)
# Central Pole
pole = cylinder(pos=vec(0, -h, 0), axis=vec(0, h, 0), radius=0.04, color=color.white)


# Objects
ball = sphere(
    pos=vec(0, 0, r),
    radius=0.06,
    color=color.red,
    make_trail=True,
    trail_color=color.yellow,
)
string = cylinder(pos=vec(0, 0, 0), axis=ball.pos, radius=0.01, color=color.white)

# Phase 1: Circular Motion
theta = 0
dt = 0.001

# Whirl around a few times before breaking at theta = 4*pi
while theta < 4 * pi:
    rate(100)
    theta += (v_mag / r) * dt
    ball.pos = vec(r * sin(theta), 0, r * cos(theta))
    string.axis = ball.pos

# Phase 2: String breaks at the point in front of the camera (x=0, z=+r)
# moving to the right (+x direction)
string.visible = False
ball.trail_color = color.red

# Velocity tangent vector at release: (+v_mag, 0, 0)
v_vector = vec(v_mag * cos(theta), 0, -v_mag * sin(theta))

while ball.pos.y > -h:
    rate(100)
    ball.pos += v_vector * dt
    v_vector.y -= g * dt

print(f"Radial Acceleration was: {v_mag**2 / r:.2f} m/s^2")
print(f"Ball final pos = {ball.pos}")

print("\n\nAnimation complete.")
scene.waitfor("click")

"""
Simulation Problem 37, page 104
Cars Motion
"""

from vpython import *

# Accelerations
a_lisa = vec(3, -2, 0)
a_jill = vec(1, 3, 0)

# Objects
lisa = sphere(pos=vector(0, 0, 0), radius=1, color=color.red, make_trail=True)
jill = sphere(pos=vector(0, 0, 0), radius=1, color=color.blue, make_trail=True)
dist_line = cylinder(
    pos=lisa.pos, axis=jill.pos - lisa.pos, radius=0.2, color=color.white
)

dt = 0.01
t = 0
while t < 5.0:
    rate(100)
    # Positions: r = 0.5 * a * t^2
    lisa.pos = 0.5 * a_lisa * t**2
    jill.pos = 0.5 * a_jill * t**2
    # Update relative distance line
    dist_line.pos = lisa.pos
    dist_line.axis = jill.pos - lisa.pos
    t += dt

# Final Results
v_lisa = a_lisa * 5
v_jill = a_jill * 5
print(f"Lisa's Relative Speed: {mag(v_lisa - v_jill):.2f} m/s")
print(f"Final Distance: {mag(lisa.pos - jill.pos):.2f} m")


################### The End ###################
print("\n\nAnimation complete.")
scene.waitfor("click")

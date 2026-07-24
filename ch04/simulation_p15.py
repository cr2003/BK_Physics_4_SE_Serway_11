"""
Simulation Problem 15, page 102
Home run
"""

from vpython import *
import sympy as sp

# --- 1 Physics solver (Using Kinematic Functions) ---
# Define SymPy symbols
v0, t = sp.symbols("v0, t", positive=True)
theta = radians(35.0)
g_mag = 9.8

# Kinematic equation 1: Horizontal Motion (x = x0 + v0x * t)
eq_x = sp.Eq(130, v0 * cos(theta) * t)

# Kinematic equation 2: Vertical Motion (y = y0 + v0y + t)
eq_y = sp.Eq(21, 1 + v0 * sin(theta) * t - 0.5 * g_mag * t**2)

# Solve the system of equations for v0 and t
# We use dict=True to easily extract the values
solutions = sp.solve([eq_x, eq_y], [v0, t], dict=True)

# Extract the numerical values
v0_val = float(solutions[0][v0])
t_val = float(solutions[0][t])

print(f"Calculated Initial Speed: {v0_val:.2f} m/s")
print(f"Calculated Time to Wall: {t_val:.2f} s")

# --- 2. VPython Animation ---
scene = canvas(
    title="Home Run: Kinematic Solver", width=800, height=600, center=vec(65, 10, 0)
)
ground = box(pos=vec(65, -0.5, 0), size=vec(210, 1, 10), color=color.green)
wall = box(pos=vector(130, 10.5, 0), size=vec(1, 21, 10), color=color.gray(0.5))

ball = sphere(pos=vec(0, 1, 0), radius=0.8, color=color.white, make_trail=True)
ball.v = vec(v0_val * cos(theta), v0_val * sin(theta), 0)
g_vec = vec(0, -g_mag, 0)

dt = 0.01
while ball.pos.y >= 0:
    rate(100)
    ball.v += g_vec * dt
    ball.pos += ball.v * dt

    # Visual cue when passing the wall
    if abs(ball.pos.x - 130) < 0.5:
        ball.color = color.yellow  # Highlight when clearing the wall
        ball.trail_color = color.red


################### The End ###################
print("\n\nAnimation complete.")
scene.waitfor("click")

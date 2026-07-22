"""
Simulation Problem 40, page 77
Collision between two trains
"""

from vpython import *

# 1. Setup up the Scene
secene = canvas(
    title="Train Collision Simulation", width=800, height=400, center=vec(50, 0, 0)
)
track = box(pos=vec(100, -1, 0), size=vec(300, 0.2, 2), color=color.gray(0.5))

# 2. Create the Trains
# Freight train (Slow, Constant Speed)
freight = box(
    pos=vec(58.5, 0, 0), size=vec(10, 2, 2), color=color.green, make_trail=False
)
v_f = 16.0

# Passenger train (Fast, Decelerating)
passenger = box(pos=vec(0, 0, 0), size=vec(8, 2, 2), color=color.red, make_trail=False)
v_p = 40.0
a_p = -3.00  # The acceleration

# 3. Simulation Variables
t = 0
dt = 0.01  # Time step

# Labels for real-time data
label_p = label(pos=vec(0, 15, 0), text="Passenger")
label_f = label(pos=vec(58.5, -15, 0), text="Freight")

print("Simulation Starting...")

# 4. Run the Animation
while passenger.pos.x < freight.pos.x:
    rate(100)  # Run at 100 iterations per second

    # Update Freight Train (Constant Velocity)
    freight.pos.x += v_f * dt

    # Update Passenger Train (Kinematics: v = v0 + at, x = x0 + vt)
    v_p += a_p * dt
    passenger.pos.x += v_p * dt

    # Update Labels
    label_p.pos = passenger.pos + vec(0, 15, 0)
    label_p.text = f"Passenger: {v_p:.1f} m/s"
    label_f.pos = freight.pos + vec(0, -15, 0)

    t += dt

# 5. Collision Results
print(f"COLLISION at time: {t:.2f} seconds")
print(f"Final Passenger Speed: {v_p:.2f} m/s")
print(f"Final Freight Speed: {v_f:.2f} m/s")

# Visual "Boom"
sphere(pos=passenger.pos, radius=3, color=color.orange, opacity=0.5)

################### The End ###################
print("\n\nEnd of program.")
scene.waitfor("click")

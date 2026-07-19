import numpy as np
import vpython as vp

# 1. Initialize the standalone window canvas
# In a pure script, this automatically launches a local browser window
scene = vp.canvas(
    title="Roller-Coaster Vector Addition",
    width=800,
    height=400,
    background=vp.color.gray(0.1),
)

# 2. Define angles in radians
theta_B = np.radians(30.0)
theta_C = np.radians(-40.0)

# 3. Define components as VPython vector objects
A = vp.vector(200, 0, 0)
B = vp.vector(135 * np.cos(theta_B), 135 * np.sin(theta_B), 0)
C = vp.vector(135 * np.cos(theta_C), 135 * np.sin(theta_C), 0)
R = A + B + C  # Resultant vector

# 4. Draw the arrows in 3D Space (Tip-to-Tail)
arrow_A = vp.arrow(
    pos=vp.vector(0, 0, 0), axis=A, color=vp.color.red, shaftwidth=4, headwidth=8
)

arrow_B = vp.arrow(pos=A, axis=B, color=vp.color.green, shaftwidth=4, headwidth=8)

arrow_C = vp.arrow(pos=A + B, axis=C, color=vp.color.blue, shaftwidth=4, headwidth=8)

arrow_R = vp.arrow(
    pos=vp.vector(0, 0, 0), axis=R, color=vp.color.yellow, shaftwidth=6, headwidth=10
)

# 5. Output the mathematical results to the console terminal
r_magnitude = R.mag
r_angle_deg = np.degrees(np.arctan2(R.y, R.x))

print("--- Vector Analysis Complete ---")
print(f"Total displacement magnitude: {r_magnitude:.2f} ft")
print(f"Direction angle: {r_angle_deg:.2f}° relative to the horizontal")

# 6. CRITICAL FOR STANDALONE: Keep the script alive so the window stays open
print("\nClose the browser tab or press Ctrl+C in the terminal to exit.")
while True:
    vp.rate(60)  # Tells VPython to check for window interactions 60 times per second

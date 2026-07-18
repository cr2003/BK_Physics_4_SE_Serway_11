from vpython import *

### Change the program to use angles from West of North, so to use standard math angle from x-axis,
# angles (90 + deg), and the x-distance is r cos(theta), y-distance r sin(theta)

# --- 1. Scene Setup ---
scene = canvas(title="Coast Guard Radar Rescue Simulation", width=800, height=600)
scene.range = 60  # View range in km
scene.background = color.black

# Labels for the axes
label(pos=vec(0, 55, 0), text="North", color=color.white, height=10)
label(pos=vec(0, -55, 0), text="South", color=color.white, height=10)
label(pos=vec(-55, 0, 0), text="West", color=color.white, height=10)
label(pos=vec(55, 0, 0), text="East", color=color.white, height=10)

# Live Timer Overlay
timer_label = label(pos=vec(0, 65, 0), text="Time: 0.00 min", box=False)

# --- 2. Define the Sinking Ship (SOS) ---
r_sink = 51.2
theta_sink = radians(90 + 36)  # 36 degrees West of North
# x = cos theta, y = sin for theta
pos_sink = vec(r_sink * cos(theta_sink), r_sink * sin(theta_sink), 0)

sinking_ship = sphere(pos=pos_sink, radius=1.5, color=color.red)
label(pos=pos_sink, text="SOS", yoffset=15, color=color.red)

# --- 3. Define Rescue Ships Data ---
# Data: (Dist from station, Angle W of N, Max Speed km/h, Color)
ship_data = [
    (36.1, 90 + 42, 30.0, color.green),  # Ship 1
    (37.3, 90 + 61, 38.0, color.cyan),  # Ship 2
    (10.2, 90 + 36, 32.0, color.yellow),  # Ship 3
    (51.2, 90 + 79, 45.0, color.orange),  # Ship 4
]

rescue_ships = []

# Initialize all ships first
for i, (r, ang, speed, col) in enumerate(ship_data):
    theta = radians(ang)
    start_pos = vec(r * cos(theta), r * sin(theta), 0)

    # Create the ship object
    ship_obj = box(pos=start_pos, size=vector(2, 2, 2), color=col, make_trail=True)
    ship_obj.speed = speed / 3600  # Convert km/h to km/s
    ship_obj.id = i + 1

    # Calculate initial velocity vector (Fixed vector math)
    displacement = pos_sink - start_pos
    ship_obj.velocity = norm(displacement) * ship_obj.speed

    rescue_ships.append(ship_obj)

# --- 4. Simulation Loop ---
dt = 2  # Time step in simulation seconds
time_elapsed = 0
active_ships = list(rescue_ships)  # Ships still moving

print("Simulation started...")

while len(active_ships) > 0:
    rate(200)  # Speed of the animation

    for ship in active_ships[
        :
    ]:  # Use [:] to safely remove items from list while looping
        # Calculate distance to target
        dist_to_sos = mag(pos_sink - ship.pos)

        if dist_to_sos > 0.4:  # Threshold to "arrive"
            # Update position: New Pos = Old Pos + (Velocity * Time)
            ship.pos += ship.velocity * dt
        else:
            # Ship has arrived
            print(
                f"Ship {ship.id} arrived! Total Time: {time_elapsed / 60:.2f} minutes"
            )
            active_ships.remove(ship)  # Remove from active movement

    # Update global timer
    time_elapsed += dt
    timer_label.text = f"Time: {time_elapsed / 60:.2f} min"

print("All ships have reached the target.")
scene.waitfor("click")
print("Window closing...")

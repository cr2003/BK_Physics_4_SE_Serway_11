import vpython as vp

# 1. Setup Canvas and Scene Configuration
scene = vp.canvas(
    title="Problem 46: Car vs. Bicycle Race (Slow-Motion Detail)",
    width=1000,
    height=500,
    background=vp.color.gray(0.1),
)

# Enable camera user controls while setting initial view angle
scene.forward = vp.vector(-0.4, -0.2, -1)

# 2. Define Physical Constants & Conversions (SI Units)
mph_to_ms = 0.44704  # 1 mph in m/s

v_car_max = 50.0 * mph_to_ms  # ~22.35 m/s
a_car = 9.00 * mph_to_ms  # ~4.02 m/s^2

v_bike_max = 20.0 * mph_to_ms  # ~8.94 m/s
a_bike = 13.0 * mph_to_ms  # ~5.81 m/s^2

t1_bike = v_bike_max / a_bike  # Acceleration phase duration (bike)
t1_car = v_car_max / a_car  # Acceleration phase duration (car)

# 3. Create Visual Elements
# Track segment corresponding to the first 4 seconds (~55 meters)
road = vp.box(
    pos=vp.vector(25, -0.5, 0),
    length=70,
    height=0.2,
    width=10,
    color=vp.color.gray(0.3),
)
lane_divider = vp.box(
    pos=vp.vector(25, -0.3, 0), length=70, height=0.05, width=0.2, color=vp.color.white
)

# Bicycle (Cyan)
bike = vp.compound(
    [
        vp.sphere(pos=vp.vector(0, 0.5, 2), radius=0.4, color=vp.color.cyan),
        vp.box(
            pos=vp.vector(0, 0.2, 2),
            length=0.8,
            height=0.4,
            width=0.2,
            color=vp.color.cyan,
        ),
    ]
)

# Car (Red)
car = vp.compound(
    [
        vp.box(
            pos=vp.vector(0, 0.5, -2),
            length=2.0,
            height=0.8,
            width=1.2,
            color=vp.color.red,
        ),
        vp.box(
            pos=vp.vector(0.2, 1.0, -2),
            length=1.0,
            height=0.5,
            width=1.0,
            color=vp.color.yellow,
        ),
    ]
)

# Telemetry Labels
label_time = vp.label(pos=vp.vector(0, 8, 0), text="", height=12, box=False)
label_lead = vp.label(pos=vp.vector(0, 6, 0), text="", height=12, box=False)


# 4. Kinematic Position Functions
def get_bike_pos(t):
    if t <= t1_bike:
        return 0.5 * a_bike * (t**2)
    else:
        return 0.5 * a_bike * (t1_bike**2) + v_bike_max * (t - t1_bike)


def get_car_pos(t):
    if t <= t1_car:
        return 0.5 * a_car * (t**2)
    else:
        return 0.5 * a_car * (t1_car**2) + v_car_max * (t - t1_car)


# 5. Animation Loop Parameters
t = 0.0
dt = 0.005  # Smaller step size for smooth animation
time_scale = 0.3  # 30% speed (Slow-Motion)

overtake_marked = False
max_lead_marked = False
max_lead_dist = 0.0

print("--- Starting Detailed Slow-Motion Simulation (0.0s to 4.0s) ---")

while t <= 4.0:
    vp.rate(int((1 / dt) * time_scale))

    # Calculate current positions
    x_bike = get_bike_pos(t)
    x_car = get_car_pos(t)
    lead_distance = x_bike - x_car

    # Update vehicle positions
    bike.pos.x = x_bike
    car.pos.x = x_car

    # DYNAMIC CAMERA FOCUS: Center on the midpoint and adjust range to frame both vehicles cleanly
    midpoint_x = (x_bike + x_car) / 2
    spread = max(abs(x_bike - x_car), 8)  # Minimum spread floor for close proximity

    scene.center = vp.vector(midpoint_x, 1, 0)
    scene.range = spread * 1.2

    # Track maximum lead distance
    if lead_distance > max_lead_dist:
        max_lead_dist = lead_distance

    # Milestone 1: Maximum Lead Marker (around t = 2.22s)
    if not max_lead_marked and t >= (v_bike_max / a_car):
        max_lead_marked = True
        vp.cylinder(
            pos=vp.vector(x_bike, 0, 2),
            axis=vp.vector(0, 4, 0),
            radius=0.1,
            color=vp.color.orange,
        )
        vp.label(
            pos=vp.vector(x_bike, 4.5, 2),
            text=f"Max Lead: {max_lead_dist * 3.28084:.1f} ft",
            color=vp.color.orange,
            height=10,
        )

    # Milestone 2: Overtake Moment Marker (around t = 3.10s)
    if not overtake_marked and lead_distance <= 0 and t > 0.5:
        overtake_marked = True
        vp.cylinder(
            pos=vp.vector(x_car, 0, 0),
            axis=vp.vector(0, 5, 0),
            radius=0.1,
            color=vp.color.green,
        )
        vp.label(
            pos=vp.vector(x_car, 5.5, 0),
            text=f"Overtake at t = {t:.2f} s",
            color=vp.color.green,
            height=12,
        )

    # Telemetry Updates
    label_time.pos = vp.vector(midpoint_x, midpoint_x * 0.1 + 8, 0)
    label_lead.pos = vp.vector(midpoint_x, midpoint_x * 0.1 + 6, 0)

    label_time.text = f"Time: {t:.2f} s"
    if lead_distance >= 0:
        label_lead.text = (
            f"Bicycle Lead: {lead_distance * 3.28084:.1f} ft ({lead_distance:.2f} m)"
        )
    else:
        label_lead.text = f"Car Lead: {abs(lead_distance) * 3.28084:.1f} ft ({abs(lead_distance):.2f} m)"

    t += dt

print("--- Race Segment Complete (Stopped at 4.0s) ---")

# Keep display window open for inspection
while True:
    vp.rate(60)

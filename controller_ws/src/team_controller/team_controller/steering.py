"""Select an open LiDAR direction with vehicle-width obstacle inflation."""
import math


def command(ranges, angle_min, increment, range_min, range_max, max_speed=1.0):
    if increment <= 0 or not math.isfinite(range_max) or range_max <= range_min:
        return 0.0, 0.0
    beams = []
    for i, value in enumerate(ranges):
        angle = angle_min + i * increment
        if abs(angle) <= math.radians(85):
            # Unknown/invalid measurements are obstacles, not free space.
            distance = min(value, range_max, 8.0) if math.isfinite(value) and value >= range_min else 0.0
            beams.append((angle, distance))
    if len(beams) < 10:
        return 0.0, 0.0
    front = [d for a, d in beams if abs(a) < math.radians(12)]
    if not front or min(front) < 0.45:
        return 0.0, 0.0
    inflated = [d for _, d in beams]
    # Extend each nearby obstacle by a 0.35 m half-width safety margin.
    for i, (_, distance) in enumerate(beams):
        if distance < 3.0:
            radius = min(len(beams), int(math.atan2(0.35, max(distance, 0.01)) / increment) + 1)
            for j in range(max(0, i-radius), min(len(beams), i+radius+1)):
                inflated[j] = min(inflated[j], distance)
    candidates = [i for i, d in enumerate(inflated) if d > 0.8]
    if not candidates:
        return 0.0, 0.0
    # Prefer substantial clearance, with a mild preference for straight travel.
    best = max(candidates, key=lambda i: min(inflated[i], 5.0) - 0.8 * abs(beams[i][0]))
    angle, clearance = beams[best][0], inflated[best]
    lookahead = max(1.0, min(clearance, 2.5))
    steering = math.atan2(2.0 * 0.33 * math.sin(angle), lookahead)
    steering = max(-0.35, min(0.35, steering))
    speed = min(max_speed, 0.6 if abs(steering) > 0.18 else 1.0, max(0.0, (min(front)-0.45)*0.8))
    return steering, speed

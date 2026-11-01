"""Pure pursuit for the officially supplied known-track centerline."""
import math


def follow(points, x, y, yaw, max_speed):
    nearest = min(range(len(points)), key=lambda i: math.hypot(points[i][0]-x, points[i][1]-y))
    deviation = math.hypot(points[nearest][0]-x, points[nearest][1]-y)
    if deviation > 1.0:
        return 0.0, 0.0
    index = nearest
    length = 0.0
    for _ in range(len(points)):
        following = (index + 1) % len(points)
        length += math.dist(points[index], points[following])
        index = following
        if length >= 1.2:
            break
    dx, dy = points[index][0]-x, points[index][1]-y
    lateral = -math.sin(yaw)*dx + math.cos(yaw)*dy
    forward = math.cos(yaw)*dx + math.sin(yaw)*dy
    if forward <= 0:
        return 0.0, 0.0
    steering = math.atan2(2*0.33*lateral, max(dx*dx+dy*dy, 0.01))
    steering = max(-0.35, min(0.35, steering))
    return steering, min(max_speed, 0.6 if abs(steering) > 0.18 else 1.0)

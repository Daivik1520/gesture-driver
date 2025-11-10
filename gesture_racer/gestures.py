import math
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class GestureOutput:
    move: str  # 'forward', 'reverse', 'brake', 'stop'
    turn: str  # 'left', 'right', 'straight'
    steering_angle: float  # degrees
    debug: str


def _calculate_steering_wheel_angle(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    h1_x, h1_y = p1
    h2_x, h2_y = p2
    dx = h2_x - h1_x
    dy = h2_y - h1_y
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    if angle_deg > 180:
        angle_deg -= 360
    elif angle_deg < -180:
        angle_deg += 360
    return angle_deg


def _calculate_hand_tilt(p1: Tuple[int, int], p2: Tuple[int, int], tilt_threshold: float) -> int:
    # Returns: -1 (left), 0 (straight), 1 (right)
    h1_x, h1_y = p1
    h2_x, h2_y = p2
    if abs(h2_x - h1_x) > 10:
        slope = (h2_y - h1_y) / (h2_x - h1_x)
        if slope > tilt_threshold:
            return 1
        elif slope < -tilt_threshold:
            return -1
    return 0


def decide_actions(
    hands: List[Tuple[int, int, str]],
    brake_distance_px: int = 100,
    tilt_threshold: float = 0.3,
    steering_gain: float = 1.5,
    max_steering_deg: float = 60.0,
    turn_deadband_deg: float = 8.0,
) -> GestureOutput:
    # hands: list of (x, y, label)
    debug_text = ""
    steering_angle = 0.0

    if len(hands) == 2:
        # Map Left/Right
        left = next(((x, y) for x, y, label in hands if label == "Left"), None)
        right = next(((x, y) for x, y, label in hands if label == "Right"), None)
        if not left or not right:
            # Fallback to order
            left = (hands[0][0], hands[0][1])
            right = (hands[1][0], hands[1][1])

        lx, ly = left
        rx, ry = right
        distance = math.hypot(lx - rx, ly - ry)

        if distance < brake_distance_px:
            move = "brake"
            # when braking, keep steering angle minimal
            turn = "straight"
            steering_angle = 0
            debug_text = f"Brake | Dist {distance:.0f}"
        else:
            # forward drive
            move = "forward"
            # continuous mapping based on the tilt angle between hands
            tilt_deg = _calculate_steering_wheel_angle(left, right)
            steering_angle = max(-max_steering_deg, min(max_steering_deg, tilt_deg * steering_gain))

            if steering_angle > turn_deadband_deg:
                turn = "right"
            elif steering_angle < -turn_deadband_deg:
                turn = "left"
            else:
                turn = "straight"
            debug_text = f"Tilt {tilt_deg:.1f}° | Steer {steering_angle:.1f}° | Dist {distance:.0f}"

    elif len(hands) == 1:
        move = "reverse"
        turn = "straight"
        steering_angle = 0
        debug_text = "Reverse | Single hand"
    else:
        move = "stop"
        turn = "straight"
        steering_angle = 0
        debug_text = "Stop | No hands"

    return GestureOutput(move=move, turn=turn, steering_angle=steering_angle, debug=debug_text)
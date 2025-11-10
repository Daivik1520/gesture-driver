from typing import Tuple


def _landmark_to_px(landmark, w: int, h: int) -> Tuple[int, int]:
    return int(landmark.x * w), int(landmark.y * h)


def compute_grip(hand_data, frame_width: int, frame_height: int, threshold_px: int = 28):
    """Compute grip (pinch) state for a hand using thumb-tip and index-tip distance.

    Returns: (is_gripping: bool, grip_strength: float)
    grip_strength is 0..1 where 1 means fully pinched (distance ~0),
    and 0 means far apart.
    """
    lm = getattr(hand_data, "landmarks", None)
    if lm is None:
        return False, 0.0

    # Mediapipe enums are inside the module; use integral indices to avoid import here:
    # THUMB_TIP = 4, INDEX_FINGER_TIP = 8
    try:
        thumb_tip = lm.landmark[4]
        index_tip = lm.landmark[8]
    except Exception:
        return False, 0.0

    tx, ty = _landmark_to_px(thumb_tip, frame_width, frame_height)
    ix, iy = _landmark_to_px(index_tip, frame_width, frame_height)

    dx = tx - ix
    dy = ty - iy
    dist = (dx * dx + dy * dy) ** 0.5

    is_grip = dist <= threshold_px
    # Normalize strength: 1 at 0 distance, 0 at >= 2*threshold
    strength = max(0.0, min(1.0, 1.0 - dist / (threshold_px * 2)))
    return is_grip, strength
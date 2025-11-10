from dataclasses import dataclass


@dataclass
class AppConfig:
    # Camera
    camera_index: int = 0
    frame_flip: bool = True

    # MediaPipe Hands
    model_complexity: int = 0
    max_num_hands: int = 2
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.6

    # Gesture thresholds
    brake_distance_px: int = 100
    turn_tilt_threshold: float = 0.3  # slope threshold

    # Steering mapping (continuous)
    steering_gain: float = 0.9  # maps hand tilt deg -> steering deg (lower = less sensitive)
    max_steering_deg: float = 60.0  # clamp steering angle
    turn_deadband_deg: float = 12.0  # within +/- deadband considered straight

    # Smoothing
    smoothing_alpha_angle: float = 0.18  # 0..1, higher = faster, lower = smoother

    # Input / control
    movement_keys = ["w", "a", "s", "d"]

    # UI
    show_debug: bool = True
    theme_name: str = "holo_flux"  # switchable: neo_green, ocean_blue, sunset_orange, cyber_purple, holo_flux
    advanced_ui: bool = True

    # Visual intensity and effects
    ui_intensity: float = 0.6  # 0..1 scales overlay glow/alpha (lower = less intense)
    particle_max: int = 80     # cap particle count
    trail_length: int = 8      # hand trail length
    grid_alpha: float = 0.05   # background grid overlay alpha
    scanlines_alpha: float = 0.06  # scanline alpha
    hex_alpha: float = 0.05    # hex grid overlay alpha

    # Background blur
    background_blur_enabled: bool = True
    background_blur_ksize: int = 21  # must be odd
    background_blur_sigma: float = 0.0

    # Handle widget
    handle_enabled: bool = True
    handle_style: str = "knob"  # knob | tbar
    handle_follow_hands: bool = True
    grip_threshold_px: int = 28
    handle_radius_px: int = 18
    handle_max_length_px: int = 40


DEFAULT_CONFIG = AppConfig()
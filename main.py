import cv2
import time

from gesture_racer.config import DEFAULT_CONFIG
from gesture_racer.camera import Camera
from gesture_racer.hand_tracking import HandTracker, HandData
from gesture_racer.input_controller import InputController
from gesture_racer.gestures import decide_actions
from gesture_racer.ui.theme import get_theme
from gesture_racer.ui.overlay import Overlay
from gesture_racer.smoothing import LowPassFilter


def run():
    cfg = DEFAULT_CONFIG
    theme_names = ["neo_green", "ocean_blue", "sunset_orange", "cyber_purple", "holo_flux", "dark_stealth", "dark_crimson", "dark_cyan"]
    try:
        theme_idx = max(0, theme_names.index(cfg.theme_name))
    except ValueError:
        theme_idx = 0
    theme = get_theme(theme_names[theme_idx])
    overlay = Overlay(
        theme,
        alpha_scale=cfg.ui_intensity,
        blur_enabled=cfg.background_blur_enabled,
        blur_ksize=cfg.background_blur_ksize,
        blur_sigma=cfg.background_blur_sigma,
        trail_len=cfg.trail_length,
        particle_max=cfg.particle_max,
        grid_alpha=cfg.grid_alpha,
        scan_alpha=cfg.scanlines_alpha,
        hex_alpha=cfg.hex_alpha,
    )
    controller = InputController(cfg.movement_keys)

    camera = Camera(index=cfg.camera_index, flip=cfg.frame_flip)
    angle_filter = LowPassFilter(alpha=cfg.smoothing_alpha_angle, initial=0.0)
    fps_filter = LowPassFilter(alpha=0.2, initial=0.0)
    last_time = time.time()

    # Live-tunable parameters
    steering_gain = cfg.steering_gain
    turn_deadband_deg = cfg.turn_deadband_deg
    smoothing_alpha = cfg.smoothing_alpha_angle
    advanced_mode = cfg.advanced_ui

    try:
        with HandTracker(
            model_complexity=cfg.model_complexity,
            max_num_hands=cfg.max_num_hands,
            min_detection_confidence=cfg.min_detection_confidence,
            min_tracking_confidence=cfg.min_tracking_confidence,
        ) as tracker:
            while True:
                frame = camera.read()

                hands: list[HandData] = tracker.process(frame)
                hands_tuples = [(h.x, h.y, h.label) for h in hands]

                actions = decide_actions(
                    hands_tuples,
                    brake_distance_px=cfg.brake_distance_px,
                    tilt_threshold=cfg.turn_tilt_threshold,
                    steering_gain=steering_gain,
                    max_steering_deg=cfg.max_steering_deg,
                    turn_deadband_deg=turn_deadband_deg,
                )

                # Apply keyboard actions
                # Smooth steering angle for more fluid visualization
                actions.steering_angle = angle_filter.update(actions.steering_angle)
                controller.apply_actions(actions.move, actions.turn)

                # Draw UI overlay
                extra = [
                    f"Gain: {steering_gain:.2f}",
                    f"Deadband: {turn_deadband_deg:.0f}°",
                    f"Smooth: {smoothing_alpha:.2f}",
                    f"Theme: {theme_names[theme_idx]}",
                    f"FPS: {fps_filter.value:.0f}",
                ]
                overlay.draw(
                    frame,
                    hands,
                    actions,
                    show_debug=cfg.show_debug,
                    extra_chips=extra,
                    draw_handles=True,
                    grip_threshold_px=cfg.grip_threshold_px,
                )

                cv2.imshow("Gesture Racer", frame)
                key = cv2.waitKey(1) & 0xFF
                # update FPS after display
                now = time.time()
                dt = max(1e-6, now - last_time)
                last_time = now
                fps = 1.0 / dt
                fps_filter.update(fps)
                if key == ord('q'):
                    break
                elif key == ord('t'):
                    # Cycle theme
                    theme_idx = (theme_idx + 1) % len(theme_names)
                    theme = get_theme(theme_names[theme_idx])
                    overlay = Overlay(
                        theme,
                        alpha_scale=cfg.ui_intensity,
                        blur_enabled=cfg.background_blur_enabled,
                        blur_ksize=cfg.background_blur_ksize,
                        blur_sigma=cfg.background_blur_sigma,
                        trail_len=cfg.trail_length,
                        particle_max=cfg.particle_max,
                        grid_alpha=cfg.grid_alpha,
                        scan_alpha=cfg.scanlines_alpha,
                        hex_alpha=cfg.hex_alpha,
                    )
                elif key == ord('m'):
                    # toggle advanced UI (reserved for future light mode)
                    advanced_mode = not advanced_mode
                elif key == ord('g'):
                    # reserved: toggle wrist handles (if needed in future)
                    pass
                elif key == ord('d'):
                    # Cycle only dark themes
                    darks = ["dark_stealth", "dark_crimson", "dark_cyan"]
                    # find next dark from current theme
                    try:
                        idx = darks.index(theme_names[theme_idx])
                        idx = (idx + 1) % len(darks)
                    except ValueError:
                        idx = 0
                    next_name = darks[idx]
                    theme_idx = theme_names.index(next_name)
                    theme = get_theme(theme_names[theme_idx])
                    overlay = Overlay(
                        theme,
                        alpha_scale=cfg.ui_intensity,
                        blur_enabled=cfg.background_blur_enabled,
                        blur_ksize=cfg.background_blur_ksize,
                        blur_sigma=cfg.background_blur_sigma,
                        trail_len=cfg.trail_length,
                        particle_max=cfg.particle_max,
                        grid_alpha=cfg.grid_alpha,
                        scan_alpha=cfg.scanlines_alpha,
                        hex_alpha=cfg.hex_alpha,
                    )
                elif key in (ord('-'), 0x2d):
                    # reduce sensitivity (gain)
                    steering_gain = max(0.2, steering_gain - 0.1)
                elif key in (ord('='), ord('+')):
                    # increase sensitivity (gain)
                    steering_gain = min(3.0, steering_gain + 0.1)
                elif key == ord('['):
                    # widen deadband
                    turn_deadband_deg = min(40.0, turn_deadband_deg + 2.0)
                elif key == ord(']'):
                    # narrow deadband
                    turn_deadband_deg = max(2.0, turn_deadband_deg - 2.0)
                elif key == ord('h'):
                    # toggle debug chips
                    cfg.show_debug = not cfg.show_debug
                elif key == ord('r'):
                    # reset tuning
                    steering_gain = cfg.steering_gain
                    turn_deadband_deg = cfg.turn_deadband_deg
                    smoothing_alpha = cfg.smoothing_alpha_angle
                    angle_filter.alpha = smoothing_alpha

    finally:
        controller.release_all()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
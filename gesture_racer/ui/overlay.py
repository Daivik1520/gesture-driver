import math
import cv2
from typing import List, Tuple
from gesture_racer.interaction import compute_grip

from .theme import Theme


class Overlay:
    def __init__(
        self,
        theme: Theme,
        alpha_scale: float = 0.6,
        blur_enabled: bool = False,
        blur_ksize: int = 21,
        blur_sigma: float = 0.0,
        trail_len: int = 12,
        particle_max: int = 120,
        grid_alpha: float = 0.06,
        scan_alpha: float = 0.10,
        hex_alpha: float = 0.06,
    ):
        self.theme = theme
        self.alpha_scale = max(0.0, min(1.0, alpha_scale))
        self.blur_enabled = blur_enabled
        self.blur_ksize = blur_ksize if blur_ksize % 2 == 1 else blur_ksize + 1
        self.blur_sigma = blur_sigma
        self.grid_alpha = grid_alpha
        self.scan_alpha = scan_alpha
        self.hex_alpha = hex_alpha

        self.font_main = cv2.FONT_HERSHEY_SIMPLEX
        self.font_small = cv2.FONT_HERSHEY_SIMPLEX
        self.frame_no = 0
        self.trails = {"Left": [], "Right": []}
        self.max_trail_len = trail_len
        # simple particle system
        self.particles = []  # list of dicts: {x,y,vx,vy,life,color}
        self.max_particles = particle_max

    def _panel(self, frame, x, y, w, h, color, alpha=0.35):
        overlay = frame.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
        a = alpha * self.alpha_scale
        cv2.addWeighted(overlay, a, frame, 1 - a, 0, frame)

    def _chip(self, frame, x, y, text, color_text, color_bg):
        # pill-style chip
        pad_x, pad_y = 12, 8
        (tw, th), _ = cv2.getTextSize(text, self.font_small, 0.6, 1)
        w = tw + pad_x * 2
        h = th + pad_y * 2
        r = h // 2
        overlay = frame.copy()
        # center rectangle
        cv2.rectangle(overlay, (x + r, y), (x + w - r, y + h), color_bg, -1)
        # rounded ends
        cv2.circle(overlay, (x + r, y + r), r, color_bg, -1)
        cv2.circle(overlay, (x + w - r, y + r), r, color_bg, -1)
        cv2.addWeighted(overlay, 0.45 * self.alpha_scale, frame, 1 - 0.45 * self.alpha_scale, 0, frame)
        # text
        cv2.putText(frame, text, (x + pad_x, y + th + pad_y - 2), self.font_small, 0.6, color_text, 1, cv2.LINE_AA)

    def _scanlines(self, frame, alpha=0.08, spacing=4):
        h, w, _ = frame.shape
        overlay = frame.copy()
        color = tuple(int(c * 0.6) for c in self.theme.bg_panel)
        for gy in range(0, h, spacing):
            cv2.line(overlay, (0, gy), (w, gy), color, 1)
        a = alpha * self.alpha_scale
        cv2.addWeighted(overlay, a, frame, 1 - a, 0, frame)

    def _hex_grid(self, frame, cell=60, parallax=(0, 0), alpha=0.08):
        # draw honeycomb-like grid with slight parallax
        h, w, _ = frame.shape
        overlay = frame.copy()
        color = tuple(int(c * 0.8) for c in self.theme.bg_panel)
        dx, dy = parallax
        dx = int(dx)
        dy = int(dy)
        r = cell // 2
        for y in range(0, h + cell, cell):
            for x in range(0, w + cell, cell):
                cx = x + ((y // cell) % 2) * r + dx
                cy = y + dy
                pts = [
                    (cx + r, cy),
                    (cx + r // 2, cy + int(0.866 * r)),
                    (cx - r // 2, cy + int(0.866 * r)),
                    (cx - r, cy),
                    (cx - r // 2, cy - int(0.866 * r)),
                    (cx + r // 2, cy - int(0.866 * r)),
                ]
                # draw hex outline
                for i in range(6):
                    p1 = pts[i]
                    p2 = pts[(i + 1) % 6]
                    cv2.line(overlay, p1, p2, color, 1)
        a = alpha * self.alpha_scale
        cv2.addWeighted(overlay, a, frame, 1 - a, 0, frame)

    def _palette_color(self, idx: int):
        pal = self.theme.palette or (self.theme.wheel_indicator,)
        return pal[idx % len(pal)]

    def _wheel(self, frame, cx, cy, radius, angle_deg):
        # Base wheel
        cv2.circle(frame, (cx, cy), radius, self.theme.wheel, 2)
        # Center line
        cv2.line(frame, (cx, 0), (cx, frame.shape[0]), (60, 60, 60), 1)

        # Indicator
        if angle_deg and abs(angle_deg) > 1:
            a = math.radians(angle_deg)
            end_x = cx + int(radius * math.sin(a))
            end_y = cy - int(radius * math.cos(a))
            # glow effect by multiple lines
            # gradient glow using palette
            for i, t in enumerate((6, 4, 2)):
                cv2.line(frame, (cx, cy), (end_x, end_y), self._palette_color(i + self.frame_no), t)

        # Futuristic arcs
        for i in range(4):
            color = self._palette_color(i)
            cv2.ellipse(frame, (cx, cy), (radius + 20 + i * 10, radius + 20 + i * 10), 0, 30, 150, color, 1)
            cv2.ellipse(frame, (cx, cy), (radius + 20 + i * 10, radius + 20 + i * 10), 0, 210, 330, color, 1)

        # Pulsing ring based on frame and angle intensity
        intensity = min(1.0, abs(angle_deg or 0) / 60.0)
        pulse = int(8 + 6 * abs(math.sin(self.frame_no * 0.08)))
        cv2.circle(frame, (cx, cy), radius + 8, self._palette_color(int(self.frame_no / 2)), pulse)

        # Rotating ticks for futuristic feel
        tick_overlay = frame.copy()
        tick_count = 24
        angle_offset = (self.frame_no % 360) * 1.2
        for i in range(tick_count):
            a = math.radians(angle_offset + i * (360 / tick_count))
            r1 = radius + 8
            r2 = radius + 24
            x1 = cx + int(r1 * math.cos(a))
            y1 = cy + int(r1 * math.sin(a))
            x2 = cx + int(r2 * math.cos(a))
            y2 = cy + int(r2 * math.sin(a))
            cv2.line(tick_overlay, (x1, y1), (x2, y2), self._palette_color(i), 1)
        cv2.addWeighted(tick_overlay, 0.25 * self.alpha_scale, frame, 1 - 0.25 * self.alpha_scale, 0, frame)

    def _hand_handle(self, frame, x, y, label, cx, cy, intensity, angle_offset_rad=0.0):
        """Draw a ring and a small interactive 'handle' attached to the wrist.

        - The handle is a short bar that rotates slightly with steering.
        - Color cycles through the palette for a lively interactive feel.
        """
        r_ring = 16
        r_handle = int(18 + 20 * intensity)

        base = math.atan2(y - cy, x - cx)
        a = base + angle_offset_rad

        # Ring around wrist
        ring_overlay = frame.copy()
        for i, t in enumerate((4, 2)):
            cv2.circle(ring_overlay, (x, y), r_ring + i * 2, self._palette_color(self.frame_no + i), t)
        cv2.addWeighted(ring_overlay, 0.45, frame, 0.55, 0, frame)

        # Handle bar (radial)
        sx = x + int((r_ring + 2) * math.cos(a))
        sy = y + int((r_ring + 2) * math.sin(a))
        ex = x + int((r_ring + r_handle) * math.cos(a))
        ey = y + int((r_ring + r_handle) * math.sin(a))

        handle_overlay = frame.copy()
        for i, t in enumerate((6, 4, 2)):
            cv2.line(handle_overlay, (sx, sy), (ex, ey), self._palette_color(self.frame_no + i), t)
        # small side spokes for grip effect
        spoke_len = max(6, int(8 * (0.5 + intensity)))
        for delta in (-0.35, 0.35):
            aa = a + delta
            px = x + int((r_ring + r_handle - 8) * math.cos(aa))
            py = y + int((r_ring + r_handle - 8) * math.sin(aa))
            qx = px + int(spoke_len * math.cos(aa + math.pi / 2))
            qy = py + int(spoke_len * math.sin(aa + math.pi / 2))
            cv2.line(handle_overlay, (px, py), (qx, qy), self._palette_color(self.frame_no + 3), 2)
        cv2.addWeighted(handle_overlay, 0.35, frame, 0.65, 0, frame)

    def draw(self, frame, hands, actions, show_debug=True, extra_chips: List[str] | None = None, draw_handles: bool = True, grip_threshold_px: int = 28):
        h, w, _ = frame.shape
        self.frame_no += 1

        # Optional background blur to reduce busy visuals
        if self.blur_enabled:
            blurred = cv2.GaussianBlur(frame, (self.blur_ksize, self.blur_ksize), self.blur_sigma)
            frame[:] = blurred

        # Background grid + scanlines + hexes for futuristic vibe
        grid_color = tuple(int(c * 0.6) for c in self.theme.bg_panel)
        for gx in range(0, w, 80):
            cv2.line(frame, (gx, 0), (gx, h), grid_color, 1)
        for gy in range(0, h, 80):
            cv2.line(frame, (0, gy), (w, gy), grid_color, 1)
        # parallax from steering
        parallax = (int(actions.steering_angle or 0), 0)
        self._hex_grid(frame, cell=70, parallax=parallax, alpha=self.hex_alpha)
        self._scanlines(frame, alpha=self.scan_alpha, spacing=6)

        # Top panel with title
        self._panel(frame, 0, 0, w, 60, self.theme.bg_panel)
        cv2.putText(frame, "Gesture Racer", (20, 40), self.font_main, 1.0, self.theme.accent, 2, cv2.LINE_AA)
        # corner braces
        cv2.line(frame, (10, 10), (120, 10), self.theme.accent, 2)
        cv2.line(frame, (10, 10), (10, 50), self.theme.accent, 2)

        # Status chips
        chip_x = 20
        chip_y = 70
        chip_gap = 10
        chips = [
            (f"Mode: Steering Wheel", self.theme.text_main, self.theme.bg_panel),
            (f"Hands: {len(hands)}", self.theme.text_main, self.theme.bg_panel),
            (f"Move: {actions.move}", self.theme.text_main, self.theme.bg_panel),
            (f"Turn: {actions.turn}", self.theme.text_main, self.theme.bg_panel),
        ]
        if extra_chips:
            for xc in extra_chips:
                chips.append((xc, self.theme.text_main, self.theme.bg_panel))
        for text, ct, cb in chips:
            self._chip(frame, chip_x, chip_y, text, ct, cb)
            chip_y += 35

        # Wheel in center
        cx, cy = w // 2, h // 2
        self._wheel(frame, cx, cy, radius=100, angle_deg=actions.steering_angle)

        # Steering intensity bar (multi-color fill)
        intensity = min(1.0, abs(actions.steering_angle or 0) / 60.0)
        bar_overlay = frame.copy()
        bar_w = int(220 * intensity)
        # gradient segments
        seg_w = 40
        for i in range(0, bar_w, seg_w):
            color = self._palette_color(i // seg_w + self.frame_no)
            cv2.rectangle(bar_overlay, (w - 260 + i, 22), (min(w - 260 + i + seg_w, w - 40), 40), color, -1)
        cv2.addWeighted(bar_overlay, 0.4 * self.alpha_scale, frame, 1 - 0.4 * self.alpha_scale, 0, frame)
        cv2.rectangle(frame, (w - 260, 22), (w - 40, 40), self.theme.bg_panel, 2)
        cv2.putText(frame, "Steer", (w - 330, 38), self.font_small, 0.6, self.theme.text_muted, 1, cv2.LINE_AA)

        # Particle effects emitted from center based on intensity
        if intensity > 0.1 and len(self.particles) < self.max_particles:
            emit_count = int(4 + 8 * intensity)
            for i in range(emit_count):
                ang = math.radians(i * (360 / max(1, emit_count)))
                speed = 2 + 3 * intensity
                vx = speed * math.cos(ang)
                vy = speed * math.sin(ang)
                self.particles.append({
                    'x': cx, 'y': cy,
                    'vx': vx, 'vy': vy,
                    'life': 18,
                    'color': self._palette_color(self.frame_no + i)
                })
        # update and draw particles
        part_overlay = frame.copy()
        survived = []
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            if 0 < p['life']:
                survived.append(p)
                size = max(1, int(4 * (p['life'] / 18)))
                cv2.circle(part_overlay, (int(p['x']), int(p['y'])), size, p['color'], -1)
        self.particles = survived
        cv2.addWeighted(part_overlay, 0.18 * self.alpha_scale, frame, 1 - 0.18 * self.alpha_scale, 0, frame)

        # Draw hand markers
        for hand_item in hands:
            # support both legacy tuple (x,y,label) and HandData objects
            if isinstance(hand_item, tuple):
                x, y, label = hand_item
                hdata = None
            else:
                x, y, label = hand_item.x, hand_item.y, hand_item.label
                hdata = hand_item
            color = (0, 0, 255) if label == "Left" else (255, 0, 0) if label == "Right" else (0, 255, 255)
            cv2.circle(frame, (x, y), 12, color, -1)
            cv2.putText(frame, label, (x - 20, y - 15), self.font_small, 0.5, color, 1, cv2.LINE_AA)
            # trails
            trail = self.trails.get(label, [])
            trail.append((x, y))
            if len(trail) > self.max_trail_len:
                trail.pop(0)
            self.trails[label] = trail
            if len(trail) > 1:
                trail_overlay = frame.copy()
                for i in range(1, len(trail)):
                    p1 = trail[i - 1]
                    p2 = trail[i]
                    c = self._palette_color(i)
                    cv2.line(trail_overlay, p1, p2, c, max(1, 4 - i // 3))
                cv2.addWeighted(trail_overlay, 0.2 * self.alpha_scale, frame, 1 - 0.2 * self.alpha_scale, 0, frame)

            # interactive wrist handles
            if draw_handles:
                delta = math.radians(actions.steering_angle or 0) * (0.6 if label == "Right" else -0.6)
                if hdata is not None:
                    is_grip, grip_strength = compute_grip(hdata, w, h, threshold_px=grip_threshold_px)
                else:
                    is_grip, grip_strength = False, 0.0
                self._hand_handle(frame, x, y, label, cx, cy, max(intensity, grip_strength), angle_offset_rad=delta)
                if is_grip:
                    cv2.putText(frame, "Grip", (x + 18, y - 18), self.font_small, 0.6, self._palette_color(self.frame_no), 1, cv2.LINE_AA)

        if len(hands) == 2:
            if isinstance(hands[0], tuple):
                p1 = (hands[0][0], hands[0][1])
                p2 = (hands[1][0], hands[1][1])
            else:
                p1 = (hands[0].x, hands[0].y)
                p2 = (hands[1].x, hands[1].y)
            # neon glow line between hands (multi-color)
            for i, t in enumerate((6, 3, 1)):
                cv2.line(frame, p1, p2, self._palette_color(i + self.frame_no), t)

        # Center reticle
        cv2.circle(frame, (cx, cy), 4, self.theme.accent, -1)
        cv2.line(frame, (cx - 12, cy), (cx - 24, cy), self.theme.accent, 2)
        cv2.line(frame, (cx + 12, cy), (cx + 24, cy), self.theme.accent, 2)
        cv2.line(frame, (cx, cy - 12), (cx, cy - 24), self.theme.accent, 2)
        cv2.line(frame, (cx, cy + 12), (cx, cy + 24), self.theme.accent, 2)

        # Footer instructions
        footer = [
            "Right Turn: Move RIGHT hand DOWN",
            "Left Turn: Move LEFT hand DOWN",
            "Brake: Bring hands CLOSE together",
            "Press 'q' to quit | Press 't' to cycle theme",
        ]
        for i, line in enumerate(footer):
            cv2.putText(frame, line, (20, h - 90 + i * 22), self.font_small, 0.6, self.theme.text_muted, 1, cv2.LINE_AA)

        if show_debug and actions.debug:
            cv2.putText(frame, actions.debug, (w - 250, 40), self.font_small, 0.6, (255, 255, 0), 1, cv2.LINE_AA)
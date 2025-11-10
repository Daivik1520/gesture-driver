from dataclasses import dataclass


@dataclass
class Theme:
    name: str
    bg_panel: tuple  # BGR color
    accent: tuple
    text_main: tuple
    text_muted: tuple
    wheel: tuple
    wheel_indicator: tuple
    palette: tuple | None = None  # optional multi-color palette (tuple of BGR colors)


NEO_GREEN = Theme(
    name="neo_green",
    bg_panel=(25, 25, 25),
    accent=(0, 230, 0),  # neon green
    text_main=(235, 255, 235),
    text_muted=(160, 200, 160),
    wheel=(70, 70, 70),
    wheel_indicator=(0, 255, 120),
    palette=((0, 255, 120), (0, 180, 255), (255, 200, 0)),
)

OCEAN_BLUE = Theme(
    name="ocean_blue",
    bg_panel=(28, 35, 70),
    accent=(0, 200, 255),  # cyan
    text_main=(230, 240, 255),
    text_muted=(170, 190, 240),
    wheel=(80, 90, 150),
    wheel_indicator=(0, 200, 255),
    palette=((0, 200, 255), (255, 120, 0), (0, 255, 180)),
)

SUNSET_ORANGE = Theme(
    name="sunset_orange",
    bg_panel=(40, 40, 60),
    accent=(255, 120, 0),  # neon orange
    text_main=(255, 240, 230),
    text_muted=(220, 200, 180),
    wheel=(85, 85, 110),
    wheel_indicator=(255, 140, 40),
    palette=((255, 140, 40), (0, 200, 255), (120, 255, 0)),
)


# Futuristic neon purple theme
CYBER_PURPLE = Theme(
    name="cyber_purple",
    bg_panel=(30, 20, 45),
    accent=(200, 50, 255),  # neon purple
    text_main=(245, 235, 255),
    text_muted=(200, 180, 220),
    wheel=(90, 60, 120),
    wheel_indicator=(255, 80, 220),
    palette=((255, 80, 220), (0, 200, 255), (255, 200, 0), (0, 255, 160)),
)

# Futuristic multi-color theme
HOLO_FLUX = Theme(
    name="holo_flux",
    bg_panel=(22, 22, 32),
    accent=(255, 80, 220),
    text_main=(240, 240, 255),
    text_muted=(190, 190, 220),
    wheel=(80, 70, 120),
    wheel_indicator=(255, 80, 220),
    palette=((255, 80, 220), (0, 200, 255), (255, 200, 0), (0, 255, 160)),
)


# Dark themes
DARK_STEALTH = Theme(
    name="dark_stealth",
    bg_panel=(18, 18, 24),
    accent=(0, 200, 180),
    text_main=(240, 250, 250),
    text_muted=(180, 200, 200),
    wheel=(40, 40, 55),
    wheel_indicator=(0, 200, 180),
    palette=((0, 200, 180), (0, 180, 255), (255, 180, 0)),
)

DARK_CRIMSON = Theme(
    name="dark_crimson",
    bg_panel=(20, 20, 20),
    accent=(0, 0, 220),  # BGR deep red accent
    text_main=(240, 240, 240),
    text_muted=(180, 180, 180),
    wheel=(50, 50, 50),
    wheel_indicator=(0, 0, 255),
    palette=((0, 0, 255), (0, 180, 255), (255, 200, 0)),
)

DARK_CYAN = Theme(
    name="dark_cyan",
    bg_panel=(16, 20, 24),
    accent=(255, 180, 0),  # amber accent
    text_main=(230, 240, 240),
    text_muted=(170, 190, 200),
    wheel=(45, 50, 55),
    wheel_indicator=(255, 180, 0),
    palette=((255, 180, 0), (0, 200, 255), (0, 255, 160)),
)


def get_theme(name: str) -> Theme:
    key = (name or "neo_green").lower()
    if key == "ocean_blue":
        return OCEAN_BLUE
    if key == "sunset_orange":
        return SUNSET_ORANGE
    if key == "cyber_purple":
        return CYBER_PURPLE
    if key == "holo_flux":
        return HOLO_FLUX
    if key == "dark_stealth":
        return DARK_STEALTH
    if key == "dark_crimson":
        return DARK_CRIMSON
    if key == "dark_cyan":
        return DARK_CYAN
    return NEO_GREEN

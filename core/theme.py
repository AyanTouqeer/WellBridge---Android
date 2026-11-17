import flet as ft


class Brand:
    """Centralized design tokens. Import these; never hardcode hex values in components."""

    # Core palette
    FOREST = "#132B1E"
    FOREST_HOVER = "#1A3A28"
    LIME = "#D8F478"
    LIME_SOFT = "#EEFAD0"
    MINT_SOFT = "#E8F7EC"

    # Surfaces
    SURFACE = "#FFFFFF"
    CANVAS = "#F8F9FA"
    BORDER = "#EEF2F0"

    # Text
    TEXT_PRIMARY = "#132B1E"
    TEXT_MUTED = "#65776C"
    TEXT_SUBTLE = "#8C9A90"

    # Status
    DANGER = "#E55353"
    DANGER_SOFT = "#FFEAEA"
    SUCCESS = "#1FA64A"
    SUCCESS_SOFT = "#E8F8EA"

    FONT_FAMILY = "Inter"


class Radius:
    SM = 12
    MD = 16
    LG = 20
    XL = 24
    PILL = 999


class Spacing:
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    XXL = 24


class Shadows:
    # Hex alpha format is #AARRGGBB; 0x0A is about 4% opacity
    CARD = ft.BoxShadow(
        spread_radius=0,
        blur_radius=24,
        color="#0A132B1E",
        offset=ft.Offset(0, 8),
    )
    FLOATING = ft.BoxShadow(
        spread_radius=0,
        blur_radius=30,
        color="#1F132B1E",
        offset=ft.Offset(0, 10),
    )


class Screen:
    WIDTH = 390
    HEIGHT = 844


def build_theme() -> ft.Theme:
    return ft.Theme(
        use_material3=True,
        font_family=Brand.FONT_FAMILY,
        scrollbar_theme=ft.ScrollbarTheme(
            thumb_visibility=False,
            track_visibility=False,
        ),
        color_scheme=ft.ColorScheme(
            primary=Brand.FOREST,
            on_primary=Brand.SURFACE,
            secondary=Brand.LIME,
            on_secondary=Brand.FOREST,
            secondary_container=Brand.LIME,
            on_secondary_container=Brand.FOREST,
            surface=Brand.SURFACE,
            on_surface=Brand.TEXT_PRIMARY,
        ),
    )

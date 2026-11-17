import flet as ft
import flet.canvas as cv

from core.theme import Brand, Radius, Screen, Spacing


class MapPin(ft.Container):
    """Forest pill with a live capacity percentage."""

    def __init__(self, percent: int, left: float, top: float):
        super().__init__(
            left=left,
            top=top,
            padding=ft.Padding(left=8, top=5, right=10, bottom=5),
            bgcolor=Brand.FOREST,
            border=ft.Border.all(2, Brand.SURFACE),
            border_radius=ft.BorderRadius.all(Radius.PILL),
            shadow=ft.BoxShadow(blur_radius=12, color="#40132B1E", offset=ft.Offset(0, 4)),
            content=ft.Row(
                spacing=4,
                tight=True,
                controls=[
                    ft.Icon(icon=ft.Icons.BOLT, size=13, color=Brand.LIME),
                    ft.Text(f"{percent}%", size=11, weight=ft.FontWeight.W_700, color=Brand.SURFACE),
                ],
            ),
        )


class MapDot(ft.Container):
    def __init__(self, left: float, top: float):
        super().__init__(
            left=left,
            top=top,
            width=22,
            height=22,
            bgcolor=Brand.FOREST,
            border=ft.Border.all(2, Brand.SURFACE),
            border_radius=ft.BorderRadius.all(Radius.PILL),
            alignment=ft.Alignment(0, 0),
            content=ft.Container(
                width=6, height=6, bgcolor=Brand.LIME, border_radius=ft.BorderRadius.all(Radius.PILL)
            ),
        )


class MapPreview(ft.Container):
    """Stylised map placeholder. Swap for a real map widget when the backend is ready."""

    def __init__(self, height: int = 200):
        width = Screen.WIDTH - 2 * Spacing.XL
        road = ft.Paint(color="#FFFFFF", stroke_width=7, stroke_cap=ft.StrokeCap.ROUND)
        side = ft.Paint(color="#F4F7F2", stroke_width=4, stroke_cap=ft.StrokeCap.ROUND)
        park = ft.Paint(color="#D5E6D0")
        water = ft.Paint(color="#DCEBE6")

        shapes = [
            cv.Rect(18, 16, 96, 58, border_radius=ft.BorderRadius.all(16), paint=park),
            cv.Rect(width - 130, height - 56, 112, 40, border_radius=ft.BorderRadius.all(20), paint=water),
            cv.Line(-10, height * 0.62, width + 10, height * 0.30, paint=road),
            cv.Line(width * 0.35, -10, width * 0.62, height + 10, paint=road),
            cv.Line(-10, height * 0.18, width * 0.55, height * 0.40, paint=side),
            cv.Line(width * 0.72, -10, width * 0.95, height + 10, paint=side),
        ]

        hint = ft.Container(
            left=0,
            right=0,
            top=12,
            alignment=ft.Alignment(0, 0),
            content=ft.Container(
                padding=ft.Padding(left=12, top=6, right=12, bottom=6),
                bgcolor="#E6FFFFFF",
                border_radius=ft.BorderRadius.all(Radius.PILL),
                content=ft.Text(
                    "Drag to explore · Select a pin",
                    size=10,
                    weight=ft.FontWeight.W_500,
                    color=Brand.TEXT_MUTED,
                ),
            ),
        )

        super().__init__(
            width=width,
            height=height,
            bgcolor="#E8EDE8",
            border_radius=ft.BorderRadius.all(Radius.XL),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            border=ft.Border.all(1, Brand.BORDER),
            content=ft.Stack(
                width=width,
                height=height,
                controls=[
                    cv.Canvas(shapes=shapes, width=width, height=height),
                    hint,
                    MapDot(left=36, top=70),
                    MapDot(left=width - 70, top=64),
                    MapDot(left=64, top=height - 48),
                    MapPin(percent=35, left=width / 2 - 28, top=height / 2 - 6),
                ],
            ),
        )
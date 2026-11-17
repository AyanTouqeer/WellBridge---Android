import flet as ft

from core.theme import Brand, Radius


class WellEAvatar(ft.Container):
    """Well E mascot: forest face, lime eyes, lime antenna dot."""

    def __init__(self, size: int = 32):
        body_top = size * 0.16
        eye_w, eye_h = max(size * 0.12, 3), max(size * 0.2, 5)
        antenna = ft.Container(
            left=size / 2 - size * 0.06,
            top=0,
            width=size * 0.12,
            height=size * 0.12,
            bgcolor=Brand.LIME,
            border_radius=ft.BorderRadius.all(Radius.PILL),
        )
        body = ft.Container(
            left=0,
            top=body_top,
            width=size,
            height=size - body_top,
            bgcolor=Brand.FOREST,
            border_radius=ft.BorderRadius.all(size * 0.3),
            alignment=ft.Alignment(0, 0),
            content=ft.Row(
                spacing=size * 0.16,
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=eye_w, height=eye_h, bgcolor=Brand.LIME,
                                 border_radius=ft.BorderRadius.all(Radius.PILL)),
                    ft.Container(width=eye_w, height=eye_h, bgcolor=Brand.LIME,
                                 border_radius=ft.BorderRadius.all(Radius.PILL)),
                ],
            ),
        )
        super().__init__(width=size, height=size, content=ft.Stack(controls=[body, antenna]))


class UserBubble(ft.Column):
    def __init__(self, text: str):
        bubble = ft.Container(
            margin=ft.Margin(left=56, top=0, right=0, bottom=0),
            padding=ft.Padding(left=14, top=10, right=14, bottom=10),
            bgcolor=Brand.LIME_SOFT,
            border=ft.Border.all(1, "#E2EFCF"),
            border_radius=ft.BorderRadius(top_left=18, top_right=4, bottom_left=18, bottom_right=18),
            content=ft.Text(text, size=13.5, weight=ft.FontWeight.W_600, color=Brand.TEXT_PRIMARY),
        )
        super().__init__(
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.END,
            controls=[bubble],
        )


class AssistantBubble(ft.Row):
    def __init__(self, text: str, muted: bool = False):
        bubble = ft.Container(
            margin=ft.Margin(left=0, top=0, right=36, bottom=0),
            padding=ft.Padding(left=14, top=10, right=14, bottom=10),
            bgcolor=Brand.SURFACE,
            border=ft.Border.all(1, Brand.BORDER),
            border_radius=ft.BorderRadius(top_left=4, top_right=18, bottom_left=18, bottom_right=18),
            content=ft.Text(
                text,
                size=13.5,
                color=Brand.TEXT_MUTED if muted else Brand.TEXT_PRIMARY,
                italic=muted,
            ),
        )
        super().__init__(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                WellEAvatar(32),
                ft.Column(spacing=0, expand=True, horizontal_alignment=ft.CrossAxisAlignment.START,
                          controls=[bubble]),
            ],
        )
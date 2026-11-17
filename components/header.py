from typing import Callable, Optional

import flet as ft

from core.theme import Brand, Radius


class IconBubble(ft.Container):
    """Round icon button with an optional lime notification dot."""

    def __init__(
            self,
            icon,
            on_click: Optional[Callable[[ft.ControlEvent], None]] = None,
            show_badge: bool = False,
    ):
        size = 40
        layers: list[ft.Control] = [
            ft.Container(
                width=size,
                height=size,
                bgcolor=Brand.MINT_SOFT,
                border_radius=ft.BorderRadius.all(Radius.PILL),
                alignment=ft.Alignment(0, 0),
                content=ft.Icon(icon=icon, size=20, color=Brand.FOREST),
            )
        ]
        if show_badge:
            layers.append(
                ft.Container(
                    width=10,
                    height=10,
                    right=8,
                    top=8,
                    bgcolor=Brand.LIME,
                    border=ft.Border.all(2, Brand.SURFACE),
                    border_radius=ft.BorderRadius.all(Radius.PILL),
                )
            )
        super().__init__(
            width=size,
            height=size,
            on_click=on_click,
            content=ft.Stack(controls=layers, width=size, height=size),
        )


class AppHeader(ft.Container):
    """Reusable top bar: leading bubble, title/subtitle, trailing bubble."""

    def __init__(
            self,
            title: str,
            subtitle: Optional[str] = None,
            leading_icon=ft.Icons.PERSON_OUTLINE,
            trailing_icon=ft.Icons.NOTIFICATIONS_NONE_OUTLINED,
            show_badge: bool = False,
            on_leading: Optional[Callable[[ft.ControlEvent], None]] = None,
            on_trailing: Optional[Callable[[ft.ControlEvent], None]] = None,
    ):
        title_controls: list[ft.Control] = [
            ft.Text(title, size=22, weight=ft.FontWeight.W_800, color=Brand.TEXT_PRIMARY)
        ]
        if subtitle:
            title_controls.append(
                ft.Text(subtitle, size=12, weight=ft.FontWeight.W_500, color=Brand.TEXT_MUTED)
            )

        super().__init__(
            padding=ft.Padding(left=20, top=12, right=20, bottom=8),
            content=ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    IconBubble(leading_icon, on_leading),
                    ft.Column(spacing=0, tight=True, expand=True, controls=title_controls),
                    IconBubble(trailing_icon, on_trailing, show_badge=show_badge),
                ],
            ),
        )
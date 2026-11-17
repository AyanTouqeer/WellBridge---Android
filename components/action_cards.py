from typing import Callable, Optional, Sequence

import flet as ft

from core.models import RoutineCard, TipsCard
from core.theme import Brand, Radius, Shadows


def _card_shell(content: ft.Control, padding: int = 14) -> ft.Container:
    return ft.Container(
        bgcolor=Brand.SURFACE,
        padding=padding,
        border=ft.Border.all(1, Brand.BORDER),
        border_radius=ft.BorderRadius.all(Radius.LG),
        shadow=Shadows.CARD,
        content=content,
    )


class TipsPanel(ft.Container):
    def __init__(self, card: TipsCard):
        header = ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=28, height=28, bgcolor=Brand.MINT_SOFT,
                    border_radius=ft.BorderRadius.all(8), alignment=ft.Alignment(0, 0),
                    content=ft.Icon(icon=ft.Icons.HEALTH_AND_SAFETY_OUTLINED, size=16, color=Brand.FOREST),
                ),
                ft.Text(card.title, size=14, weight=ft.FontWeight.W_700, color=Brand.TEXT_PRIMARY),
            ],
        )
        items = [
            ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Icon(icon=ft.Icons.CHECK_ROUNDED, size=16, color=Brand.SUCCESS),
                    ft.Text(tip, size=12.5, color=Brand.TEXT_PRIMARY, expand=True),
                ],
            )
            for tip in card.tips
        ]
        note = ft.Text(
            "Stop if you feel sharp pain. If it doesn't ease up, see a clinician.",
            size=11, color=Brand.TEXT_SUBTLE,
        )
        super().__init__(
            content=_card_shell(
                ft.Column(
                    spacing=12,
                    controls=[header, ft.Divider(height=1, color=Brand.BORDER), *items, note],
                )
            )
        )


class RoutinePanel(ft.Container):
    def __init__(self, card: RoutineCard, on_start: Optional[Callable[[ft.ControlEvent], None]] = None):
        thumb = ft.Container(
            width=88, height=88, bgcolor=Brand.FOREST,
            border_radius=ft.BorderRadius.all(14),
            content=ft.Stack(
                controls=[
                    ft.Container(
                        left=0, top=0, right=0, bottom=0, alignment=ft.Alignment(0, 0),
                        content=ft.Icon(icon=ft.Icons.SELF_IMPROVEMENT, size=36, color=Brand.LIME),
                    ),
                    ft.Container(
                        left=6, bottom=6,
                        padding=ft.Padding(left=7, top=3, right=8, bottom=3),
                        bgcolor=Brand.LIME,
                        border_radius=ft.BorderRadius.all(Radius.PILL),
                        content=ft.Row(
                            spacing=3, tight=True,
                            controls=[
                                ft.Icon(icon=ft.Icons.PLAY_ARROW_ROUNDED, size=12, color=Brand.FOREST),
                                ft.Text(f"{card.minutes} min", size=10, weight=ft.FontWeight.W_700,
                                        color=Brand.FOREST),
                            ],
                        ),
                    ),
                ]
            ),
        )
        details = ft.Column(
            spacing=6, expand=True,
            controls=[
                ft.Text(card.title, size=13.5, weight=ft.FontWeight.W_700, color=Brand.TEXT_PRIMARY),
                ft.Text(card.description, size=11.5, color=Brand.TEXT_MUTED),
                ft.Row(controls=[
                    ft.Button(
                        content=ft.Text("Start Routine", size=12, weight=ft.FontWeight.W_600),
                        on_click=on_start,
                        expand=True,
                        style=ft.ButtonStyle(
                            color=Brand.FOREST, bgcolor=Brand.LIME,
                            shape=ft.RoundedRectangleBorder(radius=Radius.SM),
                            padding=ft.Padding(left=12, top=8, right=12, bottom=8),
                        ),
                    )
                ]),
            ],
        )
        super().__init__(
            content=_card_shell(
                ft.Row(spacing=12, vertical_alignment=ft.CrossAxisAlignment.START,
                       controls=[thumb, details]),
                padding=12,
            )
        )


class SuggestionChips(ft.Row):
    """Quick replies shown under a Well E answer."""

    def __init__(self, options: Sequence[str], on_select: Callable[[str], None]):
        chips = [
            ft.Container(
                padding=ft.Padding(left=14, top=8, right=14, bottom=8),
                border=ft.Border.all(1, Brand.FOREST),
                border_radius=ft.BorderRadius.all(Radius.PILL),
                bgcolor=Brand.SURFACE,
                on_click=lambda e, o=o: on_select(o),
                content=ft.Text(o, size=12, weight=ft.FontWeight.W_600, color=Brand.FOREST),
            )
            for o in options
        ]
        super().__init__(wrap=True, spacing=8, run_spacing=8, controls=chips)
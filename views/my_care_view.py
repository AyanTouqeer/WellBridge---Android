from typing import Callable

import flet as ft

from core.routes import Tab
from core.theme import Brand, Spacing


class MyCareView(ft.Container):
    """My Care tab: credits, check-in QR, ledger."""

    def __init__(self, navigate: Callable[[Tab], None]):
        self.navigate = navigate
        super().__init__(
            expand=True,
            padding=Spacing.XL,
            content=ft.Column(
                spacing=Spacing.SM,
                controls=[
                    ft.Text("My Care", size=22, weight=ft.FontWeight.W_700, color=Brand.TEXT_PRIMARY),
                    ft.Text("Your credits and check-in", size=13, color=Brand.TEXT_MUTED),
                ],
            ),
        )
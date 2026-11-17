from typing import Callable, Optional

import flet as ft

from core.theme import Brand, Radius, Shadows, Spacing


class CreditChip(ft.Container):
    """Lime credit-cost pill, e.g. '12 cr'. Reused by cards, Well E, and booking sheets."""

    def __init__(self, credits: int):
        super().__init__(
            content=ft.Row(
                spacing=4,
                tight=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(icon=ft.Icons.MONETIZATION_ON_OUTLINED, size=14, color=Brand.FOREST),
                    ft.Text(
                        f"{credits} cr",
                        size=12,
                        weight=ft.FontWeight.W_700,
                        color=Brand.FOREST,
                    ),
                ],
            ),
            bgcolor=Brand.LIME,
            padding=ft.Padding(left=8, top=4, right=10, bottom=4),
            border_radius=ft.BorderRadius.all(Radius.PILL),
        )


class CapacityBadge(ft.Container):
    """Live capacity pill, e.g. '35% full · Room to move'."""

    def __init__(self, percent_full: int, label: str = "Room to move"):
        super().__init__(
            content=ft.Row(
                spacing=6,
                tight=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=6,
                        height=6,
                        bgcolor=Brand.SUCCESS,
                        border_radius=ft.BorderRadius.all(Radius.PILL),
                    ),
                    ft.Text(
                        f"{percent_full}% full · {label}",
                        size=10,
                        weight=ft.FontWeight.W_600,
                        color=Brand.SUCCESS,
                    ),
                ],
            ),
            bgcolor=Brand.SUCCESS_SOFT,
            padding=ft.Padding(left=8, top=3, right=8, bottom=3),
            border_radius=ft.BorderRadius.all(Radius.PILL),
        )


class FacilityCard(ft.Container):
    """
    Reusable facility card for Discover and Well E recommendation feeds.

    Args:
        name:         Facility name.
        category:     Subtitle, e.g. "Gym · Strength".
        distance:     Display string, e.g. "0.4 mi".
        credits:      Credit cost per visit.
        image_src:    Optional thumbnail URL/asset path. Falls back to an icon tile.
        percent_full: Optional live capacity; shows CapacityBadge when set.
        on_primary:   Callback for the primary button.
        on_details:   Callback for the secondary button (hidden if None).
        primary_label / details_label: Button text.
    """

    def __init__(
            self,
            name: str,
            category: str,
            distance: str,
            credits: int,
            image_src: Optional[str] = None,
            percent_full: Optional[int] = None,
            on_primary: Optional[Callable[[ft.ControlEvent], None]] = None,
            on_details: Optional[Callable[[ft.ControlEvent], None]] = None,
            primary_label: str = "Book Now",
            details_label: str = "View Details",
    ):
        self.facility_name = name
        self.category = category
        self.distance = distance
        self.credits = credits
        self.image_src = image_src
        self.percent_full = percent_full
        self.on_primary = on_primary
        self.on_details = on_details
        self.primary_label = primary_label
        self.details_label = details_label

        super().__init__(
            content=self._build_body(),
            bgcolor=Brand.SURFACE,
            padding=Spacing.MD + 2,
            border=ft.Border.all(1, Brand.BORDER),
            border_radius=ft.BorderRadius.all(Radius.LG),
            shadow=Shadows.CARD,
        )

    # ---- builders -------------------------------------------------------

    def _build_thumbnail(self) -> ft.Control:
        size = 74
        if self.image_src:
            return ft.Container(
                width=size,
                height=size,
                border_radius=ft.BorderRadius.all(Radius.SM),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Image(
                    src=self.image_src,
                    width=size,
                    height=size,
                    fit=ft.BoxFit.COVER,
                ),
            )
        return ft.Container(
            width=size,
            height=size,
            bgcolor=Brand.MINT_SOFT,
            border_radius=ft.BorderRadius.all(Radius.SM),
            alignment=ft.Alignment(0, 0),
            content=ft.Icon(icon=ft.Icons.SPA_OUTLINED, size=28, color=Brand.FOREST),
        )

    def _build_info(self) -> ft.Control:
        meta_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=4,
                    tight=True,
                    controls=[
                        ft.Icon(icon=ft.Icons.LOCATION_ON, size=12, color=Brand.TEXT_SUBTLE),
                        ft.Text(self.distance, size=11, color=Brand.TEXT_SUBTLE, weight=ft.FontWeight.W_500),
                    ],
                ),
                CreditChip(self.credits),
            ],
        )

        info_controls: list[ft.Control] = [
            ft.Text(
                self.facility_name,
                size=15,
                weight=ft.FontWeight.W_700,
                color=Brand.TEXT_PRIMARY,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
            ft.Text(
                self.category,
                size=11.5,
                weight=ft.FontWeight.W_500,
                color=Brand.TEXT_MUTED,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
        ]
        if self.percent_full is not None:
            info_controls.append(CapacityBadge(self.percent_full))
        info_controls.append(meta_row)

        return ft.Column(spacing=4, expand=True, controls=info_controls)

    def _build_actions(self) -> ft.Control:
        buttons: list[ft.Control] = []

        if self.on_details:
            buttons.append(
                ft.OutlinedButton(
                    content=ft.Text(self.details_label, size=12, weight=ft.FontWeight.W_600),
                    on_click=self.on_details,
                    expand=True,
                    style=ft.ButtonStyle(
                        color=Brand.FOREST,
                        bgcolor=Brand.CANVAS,
                        side=ft.BorderSide(1, Brand.BORDER),
                        shape=ft.RoundedRectangleBorder(radius=Radius.SM),
                        padding=ft.Padding(left=12, top=10, right=12, bottom=10),
                    ),
                )
            )

        buttons.append(
            ft.Button(
                content=ft.Text(self.primary_label, size=12, weight=ft.FontWeight.W_600),
                on_click=self.on_primary,
                expand=True,
                style=ft.ButtonStyle(
                    color=Brand.SURFACE,
                    bgcolor=Brand.FOREST,
                    shape=ft.RoundedRectangleBorder(radius=Radius.SM),
                    padding=ft.Padding(left=12, top=10, right=12, bottom=10),
                ),
            )
        )

        return ft.Row(spacing=Spacing.SM, controls=buttons)

    def _build_body(self) -> ft.Control:
        return ft.Column(
            spacing=Spacing.MD,
            tight=True,
            controls=[
                ft.Row(
                    spacing=Spacing.MD,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[self._build_thumbnail(), self._build_info()],
                ),
                ft.Divider(height=1, color=Brand.BORDER),
                self._build_actions(),
            ],
        )
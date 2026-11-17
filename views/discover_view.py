from typing import Callable

import flet as ft

from components.facility_card import FacilityCard
from components.filter_chips import FilterChips
from components.header import AppHeader
from components.map_preview import MapPreview
from core.models import Facility
from core.routes import Tab
from core.theme import Brand, Spacing

# Placeholder data. Replace with a call to your FastAPI backend.
SAMPLE_FACILITIES = [
    Facility("forma", "Forma Fitness", "Fitness", "Gym · Strength · Mobility", "0.4 mi", 8, percent_full=35),
    Facility("aura", "Aura Mental Health", "Therapy", "Therapy · Counseling", "0.9 mi", 20),
    Facility("balance", "Balance Recovery", "Recovery", "Physiotherapy · Mobility", "1.1 mi", 24, percent_full=52),
    Facility("zen", "Zen Garden Pop-up", "Pop-ups", "Mindfulness · Breathwork", "1.2 mi", 5),
]

FILTERS = [
    ("All Care", ft.Icons.GRID_VIEW_ROUNDED),
    ("Therapy", ft.Icons.PSYCHOLOGY_OUTLINED),
    ("Recovery", ft.Icons.SELF_IMPROVEMENT),
    ("Pop-ups", ft.Icons.STOREFRONT_OUTLINED),
]


class DiscoverView(ft.Container):
    """Discover tab: header, map, category chips, nearby facility cards."""

    def __init__(self, navigate: Callable[[Tab], None]):
        self.navigate = navigate
        self.cards = ft.Column(spacing=Spacing.MD)
        self._render_cards("All Care")

        body = ft.Container(
            padding=ft.Padding(left=Spacing.XL, top=Spacing.SM, right=Spacing.XL, bottom=Spacing.XXL),
            content=ft.Column(
                spacing=Spacing.LG,
                controls=[
                    MapPreview(),
                    FilterChips(FILTERS, on_change=self._on_filter),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "Nearby Wellness Places",
                                size=16,
                                weight=ft.FontWeight.W_700,
                                color=Brand.TEXT_PRIMARY,
                            ),
                            ft.TextButton(
                                content=ft.Text("See All", size=12, weight=ft.FontWeight.W_600),
                                style=ft.ButtonStyle(color=Brand.FOREST),
                            ),
                        ],
                    ),
                    self.cards,
                ],
            ),
        )

        super().__init__(
            expand=True,
            content=ft.Column(
                expand=True,
                spacing=0,
                scroll=ft.ScrollMode.HIDDEN,   # was AUTO
                controls=[
                    AppHeader("Discover", "Wellness near you", show_badge=True),
                    body,
                ],
            ),
        )

    # ---- behaviour ------------------------------------------------------

    def _render_cards(self, category: str) -> None:
        items = [f for f in SAMPLE_FACILITIES if category == "All Care" or f.category == category]
        if not items:
            self.cards.controls = [
                ft.Text("Nothing nearby in this category yet.", size=13, color=Brand.TEXT_MUTED)
            ]
            return
        self.cards.controls = [
            FacilityCard(
                name=f.name,
                category=f.subtitle,
                distance=f.distance,
                credits=f.credits,
                image_src=f.image_src,
                percent_full=f.percent_full,
                primary_label="View Facility",
                on_primary=lambda e, f=f: self._open_facility(f),
            )
            for f in items
        ]

    def _on_filter(self, category: str) -> None:
        self._render_cards(category)
        self.cards.update()

    def _open_facility(self, facility: Facility) -> None:
        print(f"open facility: {facility.id}")  # next step: push the facility detail screen
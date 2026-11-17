from typing import Callable, Optional

import flet as ft

from core.models import PlanCard, PlanStep
from core.theme import Brand, Radius, Shadows

KIND_ICONS = {
    "home": ft.Icons.ACCESSIBILITY_NEW,
    "session": ft.Icons.MEDICAL_SERVICES_OUTLINED,
    "rest": ft.Icons.SELF_IMPROVEMENT,
}


class PlanTimeline(ft.Container):
    """Multi-day plan card with day tabs, step list, and one button to book everything."""

    def __init__(
            self,
            plan: PlanCard,
            on_book_step: Optional[Callable[[PlanStep], None]] = None,
            on_book_plan: Optional[Callable[[PlanCard], None]] = None,
    ):
        self.plan = plan
        self._on_book_step = on_book_step
        self._on_book_plan = on_book_plan
        self._selected = 0

        self._tabs = [self._make_tab(i, d.label) for i, d in enumerate(plan.days)]
        self._steps = ft.Column(spacing=0)
        self._render_steps()

        total = plan.total_credits
        footer: list[ft.Control] = []
        if total > 0:
            footer = [
                ft.Button(
                    content=ft.Text(f"Book the Plan · {total} credits", size=13, weight=ft.FontWeight.W_700),
                    on_click=lambda e: self._on_book_plan(self.plan) if self._on_book_plan else None,
                    expand=True,
                    style=ft.ButtonStyle(
                        color=Brand.SURFACE, bgcolor=Brand.FOREST,
                        shape=ft.RoundedRectangleBorder(radius=Radius.PILL),
                        padding=ft.Padding(left=16, top=14, right=16, bottom=14),
                    ),
                )
            ]

        super().__init__(
            bgcolor=Brand.CANVAS,
            padding=14,
            border=ft.Border.all(1, Brand.BORDER),
            border_radius=ft.BorderRadius.all(Radius.XL),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text(plan.title, size=17, weight=ft.FontWeight.W_800, color=Brand.TEXT_PRIMARY),
                    ft.Text(plan.subtitle, size=12, color=Brand.TEXT_MUTED),
                    ft.Row(spacing=8, controls=self._tabs),
                    self._steps,
                    ft.Row(controls=footer),
                ],
            ),
        )

    # ---- tabs -----------------------------------------------------------

    def _make_tab(self, index: int, label: str) -> ft.Container:
        tab = ft.Container(
            expand=True,
            padding=ft.Padding(left=0, top=8, right=0, bottom=8),
            border_radius=ft.BorderRadius.all(Radius.PILL),
            alignment=ft.Alignment(0, 0),
            on_click=lambda e, i=index: self._select(i),
            content=ft.Text(label, size=12, weight=ft.FontWeight.W_600),
        )
        self._style_tab(tab, index == self._selected)
        return tab

    @staticmethod
    def _style_tab(tab: ft.Container, selected: bool) -> None:
        tab.bgcolor = Brand.FOREST if selected else "#EEF1EE"
        tab.content.color = Brand.SURFACE if selected else Brand.TEXT_MUTED

    def _select(self, index: int) -> None:
        if index == self._selected:
            return
        self._selected = index
        for i, tab in enumerate(self._tabs):
            self._style_tab(tab, i == index)
            tab.update()
        self._render_steps()
        self._steps.update()

    # ---- steps ----------------------------------------------------------

    def _render_steps(self) -> None:
        steps = self.plan.days[self._selected].steps
        self._steps.controls = [self._step_row(s, last=i == len(steps) - 1) for i, s in enumerate(steps)]

    def _step_row(self, step: PlanStep, last: bool) -> ft.Control:
        title_row = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Text(step.title, size=14, weight=ft.FontWeight.W_700,
                        color=Brand.TEXT_PRIMARY, expand=True),
            ],
        )
        if step.recommended:
            title_row.controls.append(
                ft.Container(
                    padding=ft.Padding(left=8, top=2, right=8, bottom=2),
                    bgcolor="#EBF7CC",
                    border_radius=ft.BorderRadius.all(Radius.PILL),
                    content=ft.Text("Recommended", size=9.5, weight=ft.FontWeight.W_700, color="#335613"),
                )
            )

        body: list[ft.Control] = [title_row, ft.Text(step.detail, size=11.5, color=Brand.TEXT_MUTED)]
        if step.credits:
            body.append(
                ft.Row(controls=[
                    ft.Button(
                        content=ft.Text(f"Book · {step.credits} credits", size=12, weight=ft.FontWeight.W_700),
                        on_click=lambda e, s=step: self._on_book_step(s) if self._on_book_step else None,
                        expand=True,
                        style=ft.ButtonStyle(
                            color=Brand.FOREST, bgcolor=Brand.LIME,
                            shape=ft.RoundedRectangleBorder(radius=Radius.PILL),
                            padding=ft.Padding(left=12, top=9, right=12, bottom=9),
                        ),
                    )
                ])
            )

        card = ft.Container(
            bgcolor=Brand.SURFACE,
            padding=12,
            border=ft.Border.all(1, Brand.BORDER),
            border_radius=ft.BorderRadius.all(Radius.MD),
            content=ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(
                        width=34, height=34, bgcolor=Brand.MINT_SOFT,
                        border_radius=ft.BorderRadius.all(Radius.PILL),
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(icon=KIND_ICONS.get(step.kind, ft.Icons.CIRCLE_OUTLINED),
                                        size=18, color=Brand.FOREST),
                    ),
                    ft.Column(spacing=5, expand=True, controls=body),
                ],
            ),
        )
        # Left border draws the timeline line between steps.
        return ft.Container(
            border=ft.Border(left=ft.BorderSide(2, Brand.LIME)),
            padding=ft.Padding(left=14, top=0, right=0, bottom=0 if last else 12),
            content=card,
        )
from typing import Callable, Optional

import flet as ft

from components.action_cards import RoutinePanel, SuggestionChips, TipsPanel
from components.chat_bubbles import AssistantBubble, UserBubble, WellEAvatar
from components.facility_card import FacilityCard
from components.header import IconBubble
from components.plan_timeline import PlanTimeline
from core.models import (
    FacilityRec, PlanCard, PlanStep, RoutineCard, TipsCard, WellEResponse,
)
from core.routes import Tab
from core.theme import Brand, Radius, Spacing
from services.well_e_service import WellEService

TRIAGE_OPTIONS = [
    ("I pulled a muscle", ft.Icons.HEALING),
    ("I need a mental reset", ft.Icons.SPA_OUTLINED),
    ("I have high energy today", ft.Icons.BOLT),
]


def _beta_tag() -> ft.Container:
    return ft.Container(
        padding=ft.Padding(left=10, top=3, right=10, bottom=3),
        bgcolor=Brand.LIME,
        border_radius=ft.BorderRadius.all(Radius.PILL),
        content=ft.Text("Beta", size=11, weight=ft.FontWeight.W_700, color=Brand.FOREST),
    )


class TriageOption(ft.Container):
    def __init__(self, label: str, icon, on_click: Callable[[ft.ControlEvent], None]):
        super().__init__(
            on_click=on_click,
            padding=ft.Padding(left=14, top=14, right=14, bottom=14),
            bgcolor=Brand.SURFACE,
            border=ft.Border.all(1, Brand.BORDER),
            border_radius=ft.BorderRadius.all(Radius.LG),
            content=ft.Row(
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=40, height=40, bgcolor=Brand.MINT_SOFT,
                        border_radius=ft.BorderRadius.all(Radius.PILL),
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(icon=icon, size=20, color=Brand.FOREST),
                    ),
                    ft.Text(label, size=14.5, weight=ft.FontWeight.W_600,
                            color=Brand.TEXT_PRIMARY, expand=True),
                    ft.Icon(icon=ft.Icons.CHEVRON_RIGHT, size=20, color=Brand.TEXT_SUBTLE),
                ],
            ),
        )


class WellEView(ft.Container):
    """Well E tab: triage hub first, then a chat feed that renders action cards."""

    def __init__(
            self,
            navigate: Callable[[Tab], None],
            credits: int = 1188,
            service: Optional[WellEService] = None,
    ):
        self.navigate = navigate
        self.credits = credits
        self.service = service or WellEService()

        self.feed = ft.Column(spacing=14, expand=True, scroll=ft.ScrollMode.HIDDEN, auto_scroll=True)
        self.input = ft.TextField(
            hint_text="Ask Well E a follow-up…",
            hint_style=ft.TextStyle(size=13.5, color=Brand.TEXT_SUBTLE),
            text_size=13.5,
            border=ft.InputBorder.NONE,
            expand=True,
            on_submit=self._on_send,
            content_padding=ft.Padding(left=16, top=10, right=8, bottom=10),
        )
        self._hub = self._build_hub()
        self._chat = self._build_chat()

        super().__init__(expand=True, content=self._hub)

    # ---- hub ------------------------------------------------------------

    def _build_hub(self) -> ft.Control:
        glow = ft.Container(
            width=200,
            height=200,
            alignment=ft.Alignment(0, 0),
            gradient=ft.RadialGradient(
                center=ft.Alignment(0, 0),
                radius=0.5,
                colors=["#66D8F478", "#00D8F478"],
            ),
            content=WellEAvatar(92),
        )
        balance = ft.Container(
            padding=14,
            bgcolor="#F3FAEA",
            border=ft.Border.all(1, "#D8EFC2"),
            border_radius=ft.BorderRadius.all(Radius.LG),
            content=ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=40, height=40, bgcolor=Brand.SURFACE,
                        border_radius=ft.BorderRadius.all(Radius.SM),
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(icon=ft.Icons.MONETIZATION_ON_OUTLINED, size=20, color=Brand.FOREST),
                    ),
                    ft.Column(
                        spacing=2, expand=True,
                        controls=[
                            ft.Text(f"You have {self.credits:,} credits", size=13.5,
                                    weight=ft.FontWeight.W_700, color=Brand.TEXT_PRIMARY),
                            ft.Text("Use them for care or wellness that Well E finds for you.",
                                    size=11.5, color=Brand.TEXT_MUTED),
                        ],
                    ),
                ],
            ),
        )
        return ft.Column(
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            controls=[
                ft.Container(
                    padding=ft.Padding(left=20, top=14, right=20, bottom=0),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(width=48),
                            ft.Text("Well E", size=17, weight=ft.FontWeight.W_800, color=Brand.TEXT_PRIMARY),
                            _beta_tag(),
                        ],
                    ),
                ),
                ft.Container(
                    padding=ft.Padding(left=24, top=6, right=24, bottom=0),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=6,
                        controls=[
                            glow,
                            ft.Text("Hey! How are you feeling?", size=24, weight=ft.FontWeight.W_800,
                                    color=Brand.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                            ft.Text("Tell me about your body or mind today. I'll find care you can book right now.",
                                    size=13, color=Brand.TEXT_MUTED, text_align=ft.TextAlign.CENTER),
                        ],
                    ),
                ),
                ft.Container(
                    padding=ft.Padding(left=20, top=22, right=20, bottom=Spacing.XXL),
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            *[TriageOption(label, icon, on_click=lambda e, l=label: self._start(l))
                              for label, icon in TRIAGE_OPTIONS],
                            ft.Container(height=6),
                            balance,
                        ],
                    ),
                ),
            ],
        )

    # ---- chat shell -----------------------------------------------------

    def _build_chat(self) -> ft.Control:
        send = ft.Container(
            width=34, height=34,
            margin=ft.Margin(left=0, top=0, right=5, bottom=0),
            bgcolor=Brand.FOREST,
            border_radius=ft.BorderRadius.all(Radius.PILL),
            alignment=ft.Alignment(0, 0),
            on_click=self._on_send,
            content=ft.Icon(icon=ft.Icons.ARROW_UPWARD_ROUNDED, size=18, color=Brand.LIME),
        )
        input_bar = ft.Container(
            padding=ft.Padding(left=16, top=8, right=16, bottom=12),
            bgcolor=Brand.SURFACE,
            border=ft.Border(top=ft.BorderSide(1, Brand.BORDER)),
            content=ft.Container(
                bgcolor=Brand.CANVAS,
                border=ft.Border.all(1, Brand.BORDER),
                border_radius=ft.BorderRadius.all(Radius.PILL),
                content=ft.Row(spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                               controls=[self.input, send]),
            ),
        )
        header = ft.Container(
            padding=ft.Padding(left=20, top=12, right=20, bottom=8),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    IconBubble(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, on_click=lambda e: self._show_hub()),
                    ft.Text("Well E", size=17, weight=ft.FontWeight.W_800, color=Brand.TEXT_PRIMARY),
                    _beta_tag(),
                ],
            ),
        )
        return ft.Column(
            expand=True,
            spacing=0,
            controls=[
                header,
                ft.Container(expand=True, padding=ft.Padding(left=16, top=8, right=16, bottom=8),
                             content=self.feed),
                input_bar,
            ],
        )

    def _show_chat(self) -> None:
        if self.content is not self._chat:
            self.content = self._chat
            self.update()

    def _show_hub(self) -> None:
        self.feed.controls.clear()
        self.content = self._hub
        self.update()

    # ---- conversation ---------------------------------------------------

    def _start(self, prompt: str) -> None:
        self.page.run_task(self._ask, prompt)

    def _on_send(self, e: ft.ControlEvent) -> None:
        text = (self.input.value or "").strip()
        if not text:
            return
        self.input.value = ""
        self.input.update()
        self.page.run_task(self._ask, text)

    async def _ask(self, text: str) -> None:
        self._show_chat()
        self.feed.controls.append(UserBubble(text))
        typing = AssistantBubble("Thinking…", muted=True)
        self.feed.controls.append(typing)
        self.feed.update()

        response = await self.service.ask(text)

        self.feed.controls.remove(typing)
        self._render_response(response)
        self.feed.update()

    def _say(self, text: str) -> None:
        self.feed.controls.append(AssistantBubble(text))
        self.feed.update()

    def _render_response(self, response: WellEResponse) -> None:
        self.feed.controls.append(AssistantBubble(response.message))
        for card in response.cards:
            self.feed.controls.append(self._render_card(card))
        if response.suggestions:
            self.feed.controls.append(
                ft.Container(
                    margin=ft.Margin(left=42, top=0, right=0, bottom=0),
                    content=SuggestionChips(response.suggestions, on_select=self._start),
                )
            )

    def _render_card(self, card) -> ft.Control:
        indent = ft.Margin(left=42, top=0, right=0, bottom=0)
        if isinstance(card, FacilityRec):
            return FacilityCard(
                name=card.name,
                category=card.subtitle,
                distance=card.distance,
                credits=card.credits,
                image_src=card.image_src,
                on_primary=lambda e, c=card: self._confirm_facility(c),
                on_details=lambda e, c=card: print(f"details: {c.name}"),  # next: facility detail screen
            )
        if isinstance(card, TipsCard):
            return ft.Container(margin=indent, content=TipsPanel(card))
        if isinstance(card, RoutineCard):
            return ft.Container(
                margin=indent,
                content=RoutinePanel(card, on_start=lambda e: self._say("The routine player is coming soon.")),
            )
        if isinstance(card, PlanCard):
            return PlanTimeline(card, on_book_step=self._confirm_step, on_book_plan=self._confirm_plan)
        return ft.Container()

    # ---- booking confirmations (replace with real booking calls) -------

    def _confirm_facility(self, card: FacilityRec) -> None:
        self._say(f"Done. {card.name} is saved for you. "
                  f"No credits are taken until you check in ({card.credits} cr).")

    def _confirm_step(self, step: PlanStep) -> None:
        self._say(f"Booked: {step.title}. No credits are taken until you check in ({step.credits} cr).")

    def _confirm_plan(self, plan: PlanCard) -> None:
        self._say(f"Your 3-day plan is booked. {plan.total_credits} credits will be used as you check in.")
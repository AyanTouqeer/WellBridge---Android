from typing import Callable, Optional, Sequence

import flet as ft

from core.theme import Brand, Radius


class FilterChip(ft.Container):
    def __init__(self, label: str, icon, selected: bool, on_click: Callable[[ft.ControlEvent], None]):
        self.label = label
        self._icon = ft.Icon(icon=icon, size=15)
        self._text = ft.Text(label, size=12, weight=ft.FontWeight.W_600)
        super().__init__(
            on_click=on_click,
            padding=ft.Padding(left=14, top=9, right=14, bottom=9),
            border_radius=ft.BorderRadius.all(Radius.MD),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            content=ft.Row(spacing=6, tight=True, controls=[self._icon, self._text]),
        )
        self.set_selected(selected, refresh=False)

    def set_selected(self, selected: bool, refresh: bool = True) -> None:
        fg = Brand.SURFACE if selected else Brand.TEXT_PRIMARY
        self.bgcolor = Brand.FOREST if selected else Brand.SURFACE
        self.border = ft.Border.all(1, Brand.FOREST if selected else Brand.BORDER)
        self._icon.color = fg
        self._text.color = fg
        if refresh:
            self.update()


class FilterChips(ft.Row):
    """Horizontally scrolling single-select chips.

    options:   [(label, icon), ...]
    on_change: called with the selected label.
    """

    def __init__(
            self,
            options: Sequence[tuple[str, object]],
            on_change: Optional[Callable[[str], None]] = None,
            selected: int = 0,
    ):
        self._on_change = on_change
        self._selected = selected
        self._chips = [
            FilterChip(label, icon, i == selected, on_click=lambda e, i=i: self._select(i))
            for i, (label, icon) in enumerate(options)
        ]
        super().__init__(spacing=10, scroll=ft.ScrollMode.HIDDEN, controls=self._chips)

    @property
    def selected_label(self) -> str:
        return self._chips[self._selected].label

    def _select(self, index: int) -> None:
        if index == self._selected:
            return
        self._chips[self._selected].set_selected(False)
        self._chips[index].set_selected(True)
        self._selected = index
        if self._on_change:
            self._on_change(self.selected_label)
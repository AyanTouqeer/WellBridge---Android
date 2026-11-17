from typing import Callable

import flet as ft

from core.routes import Tab
from core.theme import Brand, Screen, build_theme
from views.bookings_view import BookingsView
from views.discover_view import DiscoverView
from views.my_care_view import MyCareView
from views.profile_view import ProfileView
from views.well_e_view import WellEView


class WellBridgeApp:
    """Owns the page, bottom navigation, and which tab view is on screen."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.current_tab = Tab.DISCOVER

        # Views are built lazily on first visit, then cached so tab state survives switching.
        self._factories: dict[Tab, Callable[[], ft.Control]] = {
            Tab.DISCOVER: lambda: DiscoverView(navigate=self.navigate),
            Tab.BOOKINGS: lambda: BookingsView(navigate=self.navigate),
            Tab.WELL_E: lambda: WellEView(navigate=self.navigate),
            Tab.MY_CARE: lambda: MyCareView(navigate=self.navigate),
            Tab.PROFILE: lambda: ProfileView(navigate=self.navigate),
        }
        self._cache: dict[Tab, ft.Control] = {}

        self.body = ft.Container(expand=True)
        self.nav_bar = self._build_nav_bar()

        self._configure_page()
        self.page.navigation_bar = self.nav_bar
        self.page.add(ft.SafeArea(content=self.body, expand=True))
        self.navigate(Tab.DISCOVER)

    # ---- setup ----------------------------------------------------------

    def _configure_page(self) -> None:
        self.page.title = "WellBridge"
        self.page.theme = build_theme()
        self.page.bgcolor = Brand.CANVAS
        self.page.padding = 0
        self.page.window.maximized = False
        self.page.window.resizable = False
        self.page.window.width = Screen.WIDTH
        self.page.window.height = Screen.HEIGHT

    def _build_nav_bar(self) -> ft.NavigationBar:
        return ft.NavigationBar(
            selected_index=int(self.current_tab),
            on_change=self._on_nav_change,
            bgcolor=Brand.SURFACE,
            indicator_color=Brand.LIME,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.EXPLORE_OUTLINED,
                    selected_icon=ft.Icons.EXPLORE,
                    label="Discover",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.CALENDAR_MONTH_OUTLINED,
                    selected_icon=ft.Icons.CALENDAR_MONTH,
                    label="Bookings",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SMART_TOY_OUTLINED,
                    selected_icon=ft.Icons.SMART_TOY,
                    label="Well E",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
                    selected_icon=ft.Icons.ACCOUNT_BALANCE_WALLET,
                    label="My Care",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PERSON_OUTLINE,
                    selected_icon=ft.Icons.PERSON,
                    label="Profile",
                ),
            ],
        )

    # ---- navigation -----------------------------------------------------

    def _on_nav_change(self, e: ft.ControlEvent) -> None:
        self.navigate(Tab(int(e.control.selected_index)))

    def navigate(self, tab: Tab) -> None:
        """Switch tabs. Views call this too (e.g. Discover -> Well E CTA)."""
        self.current_tab = tab
        if tab not in self._cache:
            self._cache[tab] = self._factories[tab]()
        self.body.content = self._cache[tab]
        self.nav_bar.selected_index = int(tab)
        self.page.update()


def main(page: ft.Page):
    WellBridgeApp(page)


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from heartyculturenursery.components.navbar import navbar
from heartyculturenursery.components.hero import hero
from heartyculturenursery.components.product_grid import product_grid
from heartyculturenursery.pages.login import login
from heartyculturenursery.components.login_modal import login_modal


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.box(
        navbar(),
        hero(),
        product_grid(),
        login_modal(),
        width="100%",
    )


app = rx.App()
app.add_page(index)
app.add_page(login, route="/login")

import reflex as rx
import json
from .product_card import product_card

def load_products():
    try:
        with open("assets/products.json", "r") as f:
            return json.load(f)
    except Exception:
        return []

def product_grid() -> rx.Component:
    products = load_products()
    
    return rx.vstack(
        rx.heading("Our Top Selling Plants & Trees", size="7", margin_bottom="1em"),
        rx.grid(
            *[product_card(p) for p in products],
            columns="4",
            spacing="4",
            width="100%",
        ),
        width="100%",
        padding="2em 4em",
    )

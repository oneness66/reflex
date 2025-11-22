import reflex as rx

def product_card(product: dict) -> rx.Component:
    return rx.vstack(
        rx.image(
            src=product["image"],
            width="100%",
            height="250px",
            object_fit="cover",
            border_radius="5px",
        ),
        rx.text(
            product["price"],
            font_weight="bold",
            font_size="1.1em",
            margin_top="0.5em",
        ),
        rx.text(
            product["title"],
            font_size="0.9em",
            color="gray",
        ),
        width="100%",
        padding="1em",
        border="1px solid #f0f0f0",
        border_radius="8px",
        _hover={
            "box_shadow": "0 4px 12px rgba(0,0,0,0.1)",
            "transform": "translateY(-2px)",
            "transition": "all 0.2s ease-in-out",
        },
        cursor="pointer",
        align_items="start",
    )

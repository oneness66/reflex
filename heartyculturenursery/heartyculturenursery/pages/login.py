import reflex as rx
from heartyculturenursery.components.navbar import navbar
from heartyculturenursery.state import AuthState

def login() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading("Welcome Back", size="8", margin_bottom="0.5em"),
                rx.text("Please sign in to your account", color="gray", margin_bottom="2em"),
                
                rx.flex(
                    # Login Card
                    rx.card(
                        rx.vstack(
                            rx.heading("Sign In", size="5", margin_bottom="1em"),
                            
                            rx.text("Email or Mobile Number", font_weight="bold", size="2", margin_bottom="0.2em"),
                            rx.input(placeholder="user@example.com", width="100%", size="3", margin_bottom="1em"),
                            
                            rx.text("Password", font_weight="bold", size="2", margin_bottom="0.2em"),
                            rx.input(type="password", placeholder="••••••••", width="100%", size="3", margin_bottom="1.5em"),
                            
                            rx.hstack(
                                rx.checkbox("Remember me"),
                                rx.spacer(),
                                rx.link("Forgot Password?", href="#", size="2", color="blue"),
                                width="100%",
                                margin_bottom="1.5em",
                            ),
                            
                            rx.button(
                                "Sign In", 
                                width="100%", 
                                size="3", 
                                on_click=AuthState.login,
                                cursor="pointer"
                            ),
                            
                            rx.divider(margin_y="1.5em"),
                            
                            rx.button(
                                rx.hstack(
                                    rx.icon("mail", color="red"),
                                    rx.text("Sign in with Google"),
                                    align_items="center",
                                    justify="center",
                                    spacing="2",
                                ),
                                width="100%",
                                variant="outline",
                                size="3",
                                cursor="pointer",
                                on_click=AuthState.login, # Simulating login for now
                            ),
                            
                            width="100%",
                        ),
                        width=["100%", "400px"],
                        padding="2em",
                        box_shadow="lg",
                    ),
                    
                    rx.spacer(width="2em"),
                    
                    # Sign Up Section (Visual separation)
                    rx.vstack(
                        rx.heading("New Here?", size="5", margin_bottom="1em"),
                        rx.text(
                            "Create an account to checkout faster, track orders, and more.",
                            color="gray",
                            margin_bottom="2em",
                        ),
                        rx.button(
                            "Create an Account", 
                            variant="outline", 
                            size="3", 
                            width="100%",
                            cursor="pointer"
                        ),
                        width=["100%", "300px"],
                        padding="2em",
                        justify="center",
                    ),
                    
                    flex_direction=["column", "column", "row"],
                    align_items="start",
                ),
                margin_y="4em",
            ),
            width="100%",
            background_color="#fcfcfc",
            min_height="80vh",
        ),
        width="100%",
    )

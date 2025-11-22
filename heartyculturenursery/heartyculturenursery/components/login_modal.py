import reflex as rx
from heartyculturenursery.state import AuthState

def login_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            # Main content - centered white box
            rx.vstack(
                # Close button
                rx.dialog.close(
                    rx.icon("x", color="black", size=20, cursor="pointer"),
                    position="absolute",
                    top="15px",
                    right="15px",
                ),
                
                rx.heading("LOGIN", size="8", font_weight="900", margin_bottom="2em", text_align="center"),
                
                # Tabs for OTP / Google
                rx.hstack(
                    rx.button(
                        "LOGIN WITH OTP", 
                        background_color=rx.cond(AuthState.login_mode == "otp", "#00bcd4", "#f5f5f5"),
                        color=rx.cond(AuthState.login_mode == "otp", "white", "#999"),
                        font_size="0.85em", 
                        font_weight="bold",
                        padding="0.8em 1.5em",
                        border_radius="0",
                        flex="1",
                        on_click=lambda: AuthState.set_login_mode("otp"),
                        _hover={"opacity": "0.9"},
                        cursor="pointer",
                        border="none",
                    ),
                    rx.button(
                        "LOGIN WITH GOOGLE", 
                        background_color=rx.cond(AuthState.login_mode == "google", "#00bcd4", "#f5f5f5"),
                        color=rx.cond(AuthState.login_mode == "google", "white", "#999"),
                        font_size="0.85em", 
                        font_weight="bold",
                        padding="0.8em 1.5em",
                        border_radius="0",
                        flex="1",
                        on_click=lambda: AuthState.set_login_mode("google"),
                        _hover={"opacity": "0.9"},
                        cursor="pointer",
                        border="none",
                    ),
                    width="100%",
                    margin_bottom="3em",
                    spacing="0",
                    gap="0",
                ),
                
                # Conditional Form based on login_mode
                rx.cond(
                    AuthState.login_mode == "otp",
                    # OTP Form
                    rx.vstack(
                        # Show mobile input OR OTP input based on otp_sent state
                        rx.cond(
                            AuthState.otp_sent,
                            # OTP Input Section (after OTP is sent)
                            rx.vstack(
                                rx.text(
                                    f"OTP sent to +91{AuthState.mobile_number}",
                                    color="green",
                                    font_size="0.9em",
                                    margin_bottom="1.5em",
                                    text_align="center",
                                ),
                                rx.text_field(
                                    placeholder="Enter 6-digit OTP",
                                    value=AuthState.otp_code,
                                    on_change=AuthState.set_otp_code,
                                    type="text",
                                    max_length=6,
                                    width="100%",
                                    size="3",
                                    text_align="center",
                                ),
                                rx.button(
                                    "VERIFY OTP",
                                    background_color="#fdd835",
                                    color="black",
                                    font_weight="bold",
                                    width="100%",
                                    padding="1em",
                                    border_radius="0",
                                    on_click=lambda: AuthState.verify_otp(AuthState.otp_code),
                                    _hover={"background_color": "#fbc02d"},
                                    cursor="pointer",
                                    border="none",
                                    margin_top="1.5em",
                                ),
                                rx.button(
                                    "Resend OTP",
                                    variant="ghost",
                                    color="#00bcd4",
                                    margin_top="1em",
                                    on_click=lambda: AuthState.send_otp(AuthState.mobile_number),
                                    cursor="pointer",
                                ),
                                width="100%",
                            ),
                            # Mobile Number Input Section (initial state)
                            rx.vstack(
                                rx.text(
                                    "Mobile Number",
                                    font_size="0.85em",
                                    font_weight="600",
                                    color="#333",
                                    margin_bottom="0.5em",
                                    align_self="start",
                                ),
                                rx.hstack(
                                    rx.image(src="https://flagcdn.com/w40/in.png", width="30px", height="20px"),
                                    rx.text("+91", font_weight="bold", color="#333", font_size="1em"),
                                    rx.text_field(
                                        placeholder="9876543210",
                                        value=AuthState.mobile_number,
                                        on_change=AuthState.set_mobile_number,
                                        width="100%",
                                        size="3",
                                    ),
                                    align_items="center",
                                    width="100%",
                                    margin_bottom="0.5em",
                                    gap="2",
                                ),
                                
                                rx.text(
                                    "Mobile No. Without Country Code i.e 9898989898", 
                                    font_size="0.75em", 
                                    color="#666",
                                    margin_bottom="2em",
                                    align_self="start",
                                ),
                                
                                rx.text(
                                    rx.text.span("Don't have an Account? ", color="#666"),
                                    rx.text.span("Register", color="#ff9800", font_weight="bold", cursor="pointer"),
                                    font_size="0.9em",
                                    margin_bottom="2em",
                                    align_self="start",
                                ),
                                
                                rx.button(
                                    "SEND OTP",
                                    background_color="#fdd835",
                                    color="black",
                                    font_weight="bold",
                                    width="100%",
                                    padding="1.2em",
                                    border_radius="0",
                                    font_size="1em",
                                    on_click=lambda: AuthState.send_otp(AuthState.mobile_number),
                                    _hover={"background_color": "#fbc02d"},
                                    cursor="pointer",
                                    border="none",
                                ),
                                
                                width="100%",
                            ),
                        ),
                        
                        width="100%",
                    ),
                    # Google Sign-in Form
                    rx.vstack(
                        rx.vstack(
                            rx.image(
                                src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
                                width="120px",
                                margin_bottom="2em",
                            ),
                            rx.text(
                                "Sign in with your Google Account",
                                color="#666",
                                text_align="center",
                                margin_bottom="2.5em",
                                font_size="0.95em",
                            ),
                            
                            rx.button(
                                rx.hstack(
                                    rx.image(
                                        src="https://www.google.com/favicon.ico",
                                        width="20px",
                                        height="20px",
                                    ),
                                    rx.text("Continue with Gmail", font_weight="600", font_size="0.95em"),
                                    spacing="3",
                                    align_items="center",
                                    justify="center",
                                ),
                                background_color="white",
                                color="#000",
                                border="1px solid #dadce0",
                                width="100%",
                                padding="0.9em 1.5em",
                                border_radius="4px",
                                on_click=AuthState.login,
                                _hover={"box_shadow": "0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)"},
                                cursor="pointer",
                            ),
                            
                            rx.divider(margin_y="2.5em", width="100%"),
                            
                            rx.text(
                                rx.text.span("Don't have an Account? ", color="#666"),
                                rx.text.span("Register", color="#ff9800", font_weight="bold", cursor="pointer"),
                                font_size="0.9em",
                            ),
                            
                            align_items="center",
                            width="100%",
                        ),
                        
                        width="100%",
                        justify="center",
                    ),
                ),
                
                width="100%",
                max_width="500px",
                padding="3em 3em 2.5em 3em",
                align_items="center",
            ),
            padding="0",
            max_width="550px",
            width="100%",
            border_radius="8px",
            background_color="white",
        ),
        open=AuthState.show_login,
        on_open_change=AuthState.toggle_login,
    )

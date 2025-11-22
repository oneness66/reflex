import reflex as rx

class AuthState(rx.State):
    is_logged_in: bool = False
    show_login: bool = False
    login_mode: str = "otp"  # "otp" or "password"
    otp_sent: bool = False
    mobile_number: str = ""
    otp_code: str = ""

    def toggle_login(self):
        self.show_login = not self.show_login
        # Reset OTP state when closing modal
        if not self.show_login:
            self.otp_sent = False
            self.mobile_number = ""
            self.otp_code = ""

    def set_login_mode(self, mode: str):
        self.login_mode = mode
        # Reset OTP state when switching modes
        self.otp_sent = False

    def send_otp(self, mobile: str):
        """Simulate sending OTP"""
        self.mobile_number = mobile
        self.otp_sent = True
        # In a real app, you would call an API here to send SMS
        return rx.toast.success(f"OTP sent to +91{mobile}")

    def verify_otp(self, otp: str):
        """Simulate OTP verification"""
        # In a real app, you would verify against backend
        # For now, accept any 6-digit OTP
        if len(otp) == 6:
            self.is_logged_in = True
            self.show_login = False
            self.otp_sent = False
            return rx.redirect("/")
        else:
            return rx.toast.error("Invalid OTP")

    def login(self):
        self.is_logged_in = True
        self.show_login = False
        return rx.redirect("/")

    def logout(self):
        self.is_logged_in = False
        return rx.redirect("/")


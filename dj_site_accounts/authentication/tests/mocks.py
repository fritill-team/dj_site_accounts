from ..verify_phone import BaseVerifyPhoneService


class MockVerifyService(BaseVerifyPhoneService):
    def send(self):
        print(self.otp.get())

    def check(self, code):
        return self.otp.authenticate(code)


def register_callback(user):
    pass

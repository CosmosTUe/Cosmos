class MockRequest:
    def __init__(self, superuser=False):
        if superuser:
            self.user = MockSuperUser()


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True

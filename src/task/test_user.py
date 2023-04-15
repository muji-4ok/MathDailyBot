from task.user import User

class TestUser:
    def test_is_given(self):
        user = User(0)
        assert not user.is_given(None)

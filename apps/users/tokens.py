import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Generates a hash based on the primary key, timestamp and if the user is active which functions as
    a token to be used by the legacy account importing.
    """

    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk), six.text_type(timestamp) + six.text_type(user.is_active))


# Token generator used for email verification on account creation
account_activation_token = TokenGenerator()

# EMAIL activation unique tokken each user and send(link encripted with tokken) to mail and activation will return this tocken with details
#link saharing is url with an hash value
from django.contrib.auth.tokens import PasswordResetTokenGenerator
#six provide some tools to work password genarater background data
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    #tokken data what will include, hash value send accross mail
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from cinema.models import SelfToken


class TemporaryTokenAuthentication(TokenAuthentication):
    model = SelfToken

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key=key)
        if not token.last_active:
            token.last_active = timezone.now()
            token.save()
        if (timezone.now() - token.last_active).seconds > settings.INACTIVE_TIME and not user.is_superuser:
            token.delete()
            raise exceptions.AuthenticationFailed(_('Token expired'))
        else:
            token.last_active = timezone.now()
            token.save()
        return user, token

import json
import logging

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver


logger = logging.getLogger('vault.security')


def log_event(event, outcome, request=None, user=None):
    data = {
        'event': event,
        'outcome': outcome,
        'user_id': user.pk if user else None,
        'source_address': (
            request.META.get('REMOTE_ADDR')
            if request is not None
            else None
        ),
    }

    logger.info(json.dumps(data))


@receiver(user_logged_in)
def log_login_success(sender, request, user, **kwargs):
    log_event(
        event='login',
        outcome='success',
        request=request,
        user=user
    )


@receiver(user_login_failed)
def log_login_failure(sender, credentials, request, **kwargs):
    log_event(
        event='login',
        outcome='failure',
        request=request
    )


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    log_event(
        event='logout',
        outcome='success',
        request=request,
        user=user
    )
import time

from django.conf import settings


class InactivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        last = request.session.get('last_activity')
        now = int(time.time())

        if last is not None and now - last >= settings.SESSION_COOKIE_AGE:
            request.session.flush()

        if request.session.get('_auth_user_id'):
            request.session['last_activity'] = now

        response = self.get_response(request)

        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )

        response['Cache-Control'] = 'no-store'

        return response
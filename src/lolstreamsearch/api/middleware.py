from django.conf import settings

class JWTCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        return self.get_response(request)

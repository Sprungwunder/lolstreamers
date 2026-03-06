from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings

def set_cookie(response):
    response.set_cookie(
        settings.SIMPLE_JWT['AUTH_COOKIE'],
        response.data['access'],
        max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
        domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    del response.data['access']

def refresh(response):
    response.set_cookie(
        settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
        response.data['refresh'],
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
        domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    del response.data['refresh']


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access'):
            set_cookie(response)

        if response.data.get('refresh'):
            refresh(response)

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_cookie_name = settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
        refresh_token = request.COOKIES.get(refresh_cookie_name)

        if not refresh_token:
            return Response(
                {"detail": "No valid refresh token found."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access'):
            set_cookie(response)

        if response.data.get('refresh'):
            refresh(response)

        return super().finalize_response(request, response, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        response.delete_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        return response

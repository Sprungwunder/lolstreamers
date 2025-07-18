"""
URL configuration for lolstreamers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from lolstreamsearch.api.authentication import CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView
from lolstreamsearch.api.views import get_csrf_token

schema_view = get_schema_view(
    openapi.Info(
        title="lolstreamsearch API",
        default_version='v1',
        description="API-Dokumentation for lolstreamsearch",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="c.scholz@c-s-media.net"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,]
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/csrf/', get_csrf_token, name='csrf_token'),
    path('api/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/logout/', LogoutView.as_view(), name='auth_logout'),
    path("streamers/", include("lolstreamsearch.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),
        path('streamers/swagger/', schema_view.with_ui('swagger', cache_timeout=0),
             name='schema-swagger-ui'),
        path('streamers/redoc/', schema_view.with_ui('redoc', cache_timeout=0),
             name='schema-redoc'),

    ]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

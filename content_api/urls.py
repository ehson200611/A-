from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Swagger schema
schema_view = get_schema_view(
    openapi.Info(
        title="English Test API",
        default_version="v1",
        description="API барои идоракунии мундариҷаи тестҳои забони англисӣ.",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # ===================== AUTH & USERS =====================
    path("api/users/", include("users.urls")),  # 👉 Register / Login / Profile
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # JWT Login
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh JWT

    # ===================== ADMIN =====================
    path("admin/", admin.site.urls),

    # ===================== APP APIs =====================
    path("api/tests/", include("tests.urls")),                # Tests
    path("api/teachers/", include("teacher_page.urls")),      # Teachers
    path("api/homepage/", include("home_page.urls")),         # Homepage
    path("api/tests-page/", include("test_page.urls")),       # Test Page
    path("api/faqs/", include("faqs.urls")),                  # FAQs

    # ===================== DOCUMENTATION =====================
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),

    # ===================== ROOT REDIRECT =====================
    path("", RedirectView.as_view(url="/swagger/", permanent=False)),
]

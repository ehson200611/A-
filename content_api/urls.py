from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

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
    # ===================== ADMIN =====================
    path("admin/", admin.site.urls),

    # ===================== AUTH & USERS =====================
    

    # ===================== APPS =====================
    path("admin-app/", include("authenticator.urls")),    # Admin App
    path("faq/", include("faq.urls")),          # FAQs
    path("homepage/", include("home_page.urls")), # Homepage
    path("teachers/", include("teacher_page.urls")), # Teachers
    path("tests/", include("tests.urls")),        # Tests
    path("test-page/", include("test_page.urls")),# Test Page
    path("vacancy/", include("vacancy.urls")),    # Vacancy
    path("coursepage/", include("coursepage.urls")), # Course Page
    path("contact/", include("contact.urls")),            # Contacts
    path('blogs/', include('blogs.urls')),  # 👈 Register blogs API
        path('feedback/', include('feedback.urls')), 
            path('books/', include('bookpage.urls')),

    # ===================== DOCUMENTATION =====================
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),

    # ===================== ROOT REDIRECT =====================
    path("", RedirectView.as_view(url="/swagger/", permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

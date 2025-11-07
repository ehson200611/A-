from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CustomUser
from .serializers import UserRegisterSerializer


# 🔹 REGISTER VIEW
class UserRegisterView(generics.CreateAPIView):
    """
    API барои сабти корбари нав.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(
        operation_summary="Register new user",
        operation_description="Сабти корбари нав бо `username`, `number_phone`, `password`, `password_confirm`.",
        responses={201: "User created successfully"},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "number_phone": user.number_phone
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


# 🔹 LOGIN VIEW
class UserLoginView(APIView):
    """
    API барои воридшавии корбар (login).
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Login user",
        operation_description="Воридшавии корбар тавассути `username` ва `password`.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, example='ehson'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, example='12345'),
            }
        ),
        responses={200: "Login successful", 401: "Invalid credentials"},
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "number_phone": user.number_phone
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid username or password."},
                            status=status.HTTP_401_UNAUTHORIZED)


# 🔹 LOGOUT VIEW
class UserLogoutView(APIView):
    """
    API барои баромадан (logout).
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Logout user",
        operation_description="Баромадан аз система. Token-и `refresh`-ро талаб мекунад.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, example='eyJ0eXAiOiJKV1QiLCJhbGci...')
            },
            required=['refresh']
        ),
        responses={
            205: "Successfully logged out",
            400: "Invalid or missing refresh token",
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Invalid or missing refresh token."},
                            status=status.HTTP_400_BAD_REQUEST)

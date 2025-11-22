from django.urls import path
from .views import UserLoginSMSView, VerifyOTPView

urlpatterns = [
    path('login/sms/', UserLoginSMSView.as_view(), name='users_login_sms_create'),
    path('verify/otp/', VerifyOTPView.as_view(), name='verify_otp'),
]

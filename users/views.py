import random
import time
from datetime import timedelta, datetime
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserLoginSMSSerializer, VerifyOTPSerializer

def send_sms_otp(phone_number, otp):
    txn_id = int(time.time())
    params = {
        'login': settings.SMS_LOGIN,
        'str_hash': settings.SMS_HASH,
        'from': settings.SMS_SENDER,
        'phone_number': phone_number,
        'msg': f"Ваш код подтверждения: {otp}",
        'txn_id': txn_id
    }
    try:
        response = requests.get(settings.SMS_SERVER, params=params, timeout=10)
        print(response.text)
        return response.text
    except requests.RequestException as e:
        print("Error sending SMS:", e)
        return str(e)

class UserLoginSMSView(APIView):
    def post(self, request):
        serializer = UserLoginSMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = str(random.randint(100000, 999999))
            user, created = User.objects.get_or_create(phone_number=phone_number, username=phone_number)
            user.otp_code = otp
            user.otp_created_at = datetime.now()
            user.save()
            send_sms_otp(phone_number, otp)
            return Response({"message": "OTP sent to your phone."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(phone_number=phone_number)
                # Код эътибор дорад танҳо 5 дақиқа
                if user.otp_code == otp and datetime.now() - user.otp_created_at < timedelta(minutes=5):
                    user.set_password(otp)  # Агар хоҳед, паролро дар OTP гузоред
                    user.save()
                    return Response({"message": "OTP verified. Login successful."})
                return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

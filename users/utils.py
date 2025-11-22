# users/utils.py
import requests
import random
from django.conf import settings

def send_sms_otp(phone_number):
    otp = random.randint(100000, 999999)
    params = {
        'login': settings.SMS_LOGIN,
        'hash': settings.SMS_HASH,
        'sender': settings.SMS_SENDER,
        'to': phone_number,
        'message': f"Ваш код подтверждения: {otp}"
    }
    try:
        response = requests.get(settings.SMS_SERVER, params=params, timeout=5)
        # response.text метавонад матни ҷавоб аз сервер бошад
        return otp, response.text
    except requests.RequestException as e:
        # Агар хато рӯй диҳад
        return otp, str(e)

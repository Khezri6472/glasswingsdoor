from django.shortcuts import render
from allauth.account.forms import LoginForm, SignupForm

from django.shortcuts import get_object_or_404
import random
import string
from django.contrib.auth import login

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CustomUser
import datetime
from django.conf import settings
from kavenegar import KavenegarAPI, APIException, HTTPException


def combined_auth_view(request):
    login_form = LoginForm()
    signup_form = SignupForm()
    return render(request, 'account/login_signup.html', {
        'login_form': login_form,
        'signup_form': signup_form
    })


def generate_otp(self):
    code = str(random.randint(1000, 9999))
    self.otp_code = code
    self.otp_created = timezone.now()
    self.save(update_fields=["otp_code", "otp_created"])
    return code



class SendOTP(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        if not phone:
            return Response({"error": "phone is required"}, status=status.HTTP_400_BAD_REQUEST)

        # گرفتن یا ساخت کاربر
        user, created = CustomUser.objects.get_or_create(phone=phone, defaults={
            "username": phone  # اگر username لازم است
        })

        # تولید OTP
        otp_code = user.generate_otp()

        # ارسال پیامک با Kavenegar
        try:
            api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
            params = {
                'sender': '9982005114',  # شماره فرستنده که از Kavenegar داری
                'receptor': phone,     # شماره موبایل کاربر
                'message': f'کد ورود شما: {otp_code}'
            }
            response = api.sms_send(params)
            print(response)  # برای debug
        except APIException as e:
            return Response({"error": "SMS API error", "detail": str(e)}, status=500)
        except HTTPException as e:
            return Response({"error": "HTTP error", "detail": str(e)}, status=500)

        return Response({"message": "OTP sent successfully"}, status=200)

class VerifyOTP(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        otp = request.data.get("otp")

        if not phone or not otp:
            return Response({"error": "phone and otp required"}, status=400)

        try:
            user = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            return Response({"error": "user not found"}, status=404)

        if user.otp_code != otp:
            return Response({"error": "OTP invalid"}, status=400)

        if timezone.now() - user.otp_created > datetime.timedelta(minutes=2):
            return Response({"error": "OTP expired"}, status=400)

        # پاک کردن OTP
        user.otp_code = None
        user.otp_created = None
        user.save(update_fields=["otp_code", "otp_created"])

        # لاگین با مشخص کردن backend
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return Response({"message": "logged in"}, status=200)
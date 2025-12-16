
from django.urls import path
from .views import combined_auth_view, SendOTP, VerifyOTP

urlpatterns = [
    path("combined/", combined_auth_view, name="combined_auth"),
    path("send-otp/", SendOTP.as_view(), name="send_otp"),
    path("verify-otp/", VerifyOTP.as_view(), name="verify_otp"),
   
]



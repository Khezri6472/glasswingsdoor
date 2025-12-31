
from django.urls import path
from .views import combined_auth_view, SendOTP, VerifyOTP,CustomLogoutView,CreateOrUpdateAffiliateUser

urlpatterns = [
    path("combined/", combined_auth_view, name="combined_auth"),
    path("send-otp/", SendOTP.as_view(), name="send_otp"),
    path("verify-otp/", VerifyOTP.as_view(), name="verify_otp"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("api/affiliate-user/", CreateOrUpdateAffiliateUser.as_view(), name='affiliate_user_api'),
   
]



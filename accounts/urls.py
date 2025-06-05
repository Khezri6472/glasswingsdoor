
from django.urls import path
from .views import combined_auth_view

urlpatterns = [
    path("accounts/combined/", combined_auth_view, name="combined_auth"),
]

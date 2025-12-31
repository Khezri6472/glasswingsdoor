from rest_framework.permissions import BasePermission
from django.conf import settings


class HasAffiliateAPIKey(BasePermission):
    """
    Check X-API-KEY header
    """

    def has_permission(self, request, view):
        api_key = request.headers.get("X-API-KEY")
        return bool(api_key and api_key == settings.AFFILIATE_USER_API_KEY)

from rest_framework.permissions import BasePermission
from django.conf import settings

class HasExcelAPIKey(BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get("X-API-KEY")
        return api_key and api_key == settings.EXCEL_API_KEY

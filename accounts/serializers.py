from rest_framework import serializers


class AffiliateUserSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    full_name = serializers.CharField(required=False, allow_blank=True)
    user_code = serializers.CharField(max_length=10)
    is_affiliate = serializers.BooleanField(default=True)

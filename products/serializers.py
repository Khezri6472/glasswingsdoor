from rest_framework import serializers

class ProductLinkSerializer(serializers.Serializer):
    product_codes = serializers.ListField(
        child=serializers.CharField()
    )

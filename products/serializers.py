from rest_framework import serializers
from .models import ExcelFile


class ProductLinkSerializer(serializers.Serializer):
    product_codes = serializers.ListField(
        child=serializers.CharField()
    )


class ExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFile
        fields = ["file"]

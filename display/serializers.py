from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["merchant"] 

    def create(self, validated_data):
        request = self.context.get("request") 
        if request and hasattr(request, "user"):
            validated_data["merchant"] = request.user
        else:
            raise serializers.ValidationError("Merchant information is missing.")
        return super().create(validated_data)


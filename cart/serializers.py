from rest_framework import serializers
from .models import Cart , OrderDone

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity']

class OrderDoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDone
        fields = ['id', 'total_amount', 'created_at', 'products', 'intent', 'refund_status', 'is_refunded']

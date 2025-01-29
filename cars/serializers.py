from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Car, Order, CarImage

# this data i need from the user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ('id', 'image_url', 'is_primary')

class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Car
        fields = ('id', 'name', 'make', 'model', 'year', 'price', 'available',
                 'description', 'image_url', 'images', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def validate_year(self, value):
        """
        Check that the year is reasonable
        """
        current_year = 2024  # You might want to get this dynamically am out of time
        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError(f"Year must be between 1900 and {current_year + 1}")
        return value

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(),
        write_only=True,
        source='car'
    )

    class Meta:
        model = Order
        fields = ('id', 'user', 'car', 'car_id', 'status', 'order_date',
                 'last_updated', 'total_amount', 'notes')
        read_only_fields = ('status', 'order_date', 'last_updated', 'total_amount')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 
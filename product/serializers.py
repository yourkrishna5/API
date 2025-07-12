from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Product, Info

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    image = Base64ImageField()  # 👈 Base64 support

    class Meta:
        model = Product
        fields = '__all__'


# Info Serializer
class InfoSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField()  # 👈 Base64 support

    class Meta:
        model = Info
        fields = '__all__'


# Name and Profile Pic only
class InfoNamePicSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField()  # 👈 Base64 support

    class Meta:
        model = Info
        fields = ['name', 'profile_picture']
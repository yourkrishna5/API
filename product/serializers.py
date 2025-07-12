from rest_framework import serializers
from .models import Product, Info, Comments


# ---------- Product Serializers ----------
class ProductSerializer(serializers.ModelSerializer):
    # Replace 'image' with 'image_url' as a simple URL field
    image_url = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Product
        fields = ['title', 'condition', 'brand', 'image_url']


# ---------- Info Serializers ----------
class InfoSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Info
        fields = '__all__'


class InfoNamePicSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Info
        fields = ['name', 'profile_picture_url']


# ---------- Comment Serializer ----------
class Cserializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ['name']  # Assuming set automatically in view
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Product, Info, Comments


# ---------- Product Serializers ----------
class ProductSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Product
        fields = ['title', 'condition', 'brand', 'image']


# ---------- Info Serializers ----------
class InfoSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField()

    class Meta:
        model = Info
        fields = '__all__'


class InfoNamePicSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField()

    class Meta:
        model = Info
        fields = ['name', 'profile_picture']


# ---------- Comment Serializer ----------
class Cserializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ['name']  # assuming you set this automatically in the view
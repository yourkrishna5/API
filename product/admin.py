from django.contrib import admin
from .models import Product
# Register your models here.
admin.site.register(Product)
from django.contrib import admin
from rest_framework.authtoken.models import Token

admin.site.register(Token)
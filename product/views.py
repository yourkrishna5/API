from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from .firebase_auth import get_uid_from_token

class ProductCreateView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return Response({'error': 'Token missing'}, status=401)

        try:
            uid = get_uid_from_token(token)
        except:
            return Response({'error': 'Invalid token'}, status=401)

        data = request.data.copy()
        data['uploader_id'] = uid

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
from rest_framework.views import APIView
from rest_framework.response import Response

class ApiHomeView(APIView):
    def get(self, request):
        return Response({
            "message": "Welcome to the Firebase API!",
            "endpoint": {
                "/create/": "Create a product with Firebase UID"
            },
            "how_to_use": "Send Firebase idToken in Authorization header as 'Bearer <token>'"
        })
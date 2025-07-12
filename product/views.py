from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.exceptions import NotFound
from .models import Product, Info, Comments
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    InfoSerializer,
    InfoNamePicSerializer,
    Cserializer,
)
from .firebase_auth import get_uid_from_token

from .supabase_client import supabase  # Your supabase client instance
from django.conf import settings


# ---------- Product Create View with Supabase upload ----------
class ProductCreateView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if not token:
            return Response({'error': 'Token missing'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            uid = get_uid_from_token(token)
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'Image file is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Upload image to Supabase Storage
        file_path = f"products/{image_file.name}"
        try:
            supabase.storage.from_("products").upload(file_path, image_file)
            public_url = supabase.storage.from_("products").get_public_url(file_path)
        except Exception as e:
            return Response({'error': f"Upload failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = request.data.copy()
        data['uploader_id'] = uid
        data['image_url'] = public_url  # Save the Supabase public URL

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------- Info Create and List View with Supabase upload ----------
class InfoView(APIView):
    def post(self, request):
        image_file = request.FILES.get('profile_picture')
        if not image_file:
            return Response({'error': 'Profile picture file is required'}, status=status.HTTP_400_BAD_REQUEST)

        file_path = f"info/{image_file.name}"
        try:
            supabase.storage.from_("info").upload(file_path, image_file)
            public_url = supabase.storage.from_("info").get_public_url(file_path)
        except Exception as e:
            return Response({'error': f"Upload failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = request.data.copy()
        data['profile_picture_url'] = public_url  # Save Supabase public URL

        serializer = InfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Info saved successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        info_list = Info.objects.all()
        serializer = InfoNamePicSerializer(info_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------- API Home ----------
class ApiHomeView(APIView):
    def get(self, request):
        return Response(
            {
                "message": "Welcome to the Firebase API!",
                "endpoints": {
                    "/create/": "POST: Create a product with Firebase UID",
                    "/info/": "POST: Save Info | GET: List Info with name and profile pic",
                    "/<product_id>/comments/": "GET/POST comments for a specific product"
                },
                "how_to_use": "Send Firebase ID token in Authorization header as 'Bearer <token>'"
            },
            status=status.HTTP_200_OK,
        )


# ---------- Product Detail View ----------
class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


# ---------- Comment List/Create by Product ----------
class ProductCommentView(ListCreateAPIView):
    serializer_class = Cserializer

    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        if not Product.objects.filter(pk=product_id).exists():
            raise NotFound("Product not found")
        return Comments.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('pk')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found")
        serializer.save(product=product)
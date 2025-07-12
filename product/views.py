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
    Cserializer,  # kept your original name
)
from .firebase_auth import get_uid_from_token


# ---------- Product Create View ----------
class ProductCreateView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if not token:
            return Response({'error': 'Token missing'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            uid = get_uid_from_token(token)
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        data['uploader_id'] = uid

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------- Info Create and List View ----------
class InfoView(APIView):
    def post(self, request):
        serializer = InfoSerializer(data=request.data)
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
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from .models import Product, Info, Comments
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    InfoSerializer,
    InfoNamePicSerializer,
    Cserializer,  # kept your original serializer name
)
from .firebase_auth import get_uid_from_token


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


class ApiHomeView(APIView):
    def get(self, request):
        return Response(
            {
                "message": "Welcome to the Firebase API!",
                "endpoints": {
                    "/create/": "POST: Create a product with Firebase UID",
                    "/info/": "POST: Save Info | GET: List Info with name and profile pic",
                },
                "how_to_use": "Send Firebase ID token in Authorization header as 'Bearer <token>'",
            },
            status=status.HTTP_200_OK,
        )


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class CommentListCreateView(ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = Cserializer
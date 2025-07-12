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
        except Exception:
            return Response({'error': 'Invalid token'}, status=401)

        data = request.data.copy()
        data['uploader_id'] = uid  # Make sure your model has `uploader_id` field

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ApiHomeView(APIView):
    def get(self, request):
        return Response({
            "message": "Welcome to the Firebase API!",
            "endpoint": {
                "/create/": "Create a product with Firebase UID"
            },
            "how_to_use": "Send Firebase idToken in Authorization header as 'Bearer <token>'"
  
      })

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Info
from .serializers import InfoSerializer, InfoNamePicSerializer

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
        return Response(serializer.data
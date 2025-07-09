from django.urls import path
from .views import ProductCreateView, ApiHomeView
from rest_framework.authtoken import views

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('', ApiHomeView.as_view(), name='home-doc'),
    path('api-token-auth/', views.obtain_auth_token),  # Token auth endpoint
]
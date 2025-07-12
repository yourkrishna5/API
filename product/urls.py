from django.urls import path
from .views import ProductCreateView, ApiHomeView, InfoView, ProductDetailView
from rest_framework.authtoken import views

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # New detail endpoint
    path('', ApiHomeView.as_view(), name='home-doc'),
    path('api-token-auth/', views.obtain_auth_token),
    path('info/', InfoView.as_view(), name='info'),
]
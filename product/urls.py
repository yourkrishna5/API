from django.urls import path
from .views import (
    ApiHomeView,
    ProductCreateView,
    InfoView,
    ProductDetailView,
    ProductCommentView,
)

urlpatterns = [
    path('', ApiHomeView.as_view(), name='api-home'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('info/', InfoView.as_view(), name='info'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/comments/', ProductCommentView.as_view(), name='product-comments'),
]
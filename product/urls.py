from django.urls import path
from .views import ProductCreateView,ApiHomeView

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
        path('', ApiHomeView.as_view(), name='home-doc'),
]
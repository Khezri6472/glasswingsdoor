from django.urls import path

from .views import ProductListView,ProductDetailView,ProductByCategoryView,CommentCreateView

urlpatterns = [
    path('', ProductListView.as_view(),name='products'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('comment/<int:product_id>/', CommentCreateView.as_view(), name='comment_create'),

     path('category/<int:category_id>/', ProductByCategoryView.as_view(), name='products_by_category'),
]
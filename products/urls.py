from django.urls import path,re_path

from .views import ProductListView,ProductDetailView,ProductByCategoryView,CommentCreateView,ProductSearchListView,SearchSuggestionsView

urlpatterns = [
    path('', ProductListView.as_view(),name='products'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('comment/<int:product_id>/', CommentCreateView.as_view(), name='comment_create'),
     re_path(r'^products/category/(?P<slug>[-\w\u0600-\u06FF]+)/$', 
            ProductByCategoryView.as_view(), 
            name='products_by_category'),

    path('search/', ProductSearchListView.as_view(), name='search_results'),
    path("search/suggestions/", SearchSuggestionsView.as_view(), name="search_suggestions")

    # path('category/<slug:slug>/', ProductByCategoryView.as_view(), name='products_by_category'),
    #  path('category/<int:category_id>/', ProductByCategoryView.as_view(), name='products_by_category'),
]
from django.urls import path,re_path

from .views import ProductListView,ProductDetailView,ProductByCategoryView,CommentCreateView,ProductSearchListView,SearchSuggestionsView,UpdatePriceAPI, UpdateStockAPI,HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(),name='products'),
    path('products/', ProductListView.as_view(), name='product_list'),
    re_path(r'^products/category/(?P<slug>[-\w\u0600-\u06FF]+)/$', 
            ProductByCategoryView.as_view(), 
            name='products_by_category'),

    path('product/<path:slug>/<str:unit_code>/', ProductDetailView.as_view(), name='product_detail'),
    path('comment/<int:product_id>/', CommentCreateView.as_view(), name='comment_create'),
     
    path('search/', ProductSearchListView.as_view(), name='search_results'),
    path("search/suggestions/", SearchSuggestionsView.as_view(), name="search_suggestions"),

    path('api/update-price/', UpdatePriceAPI.as_view(), name='update_price_api'),
    path('api/update-stock/', UpdateStockAPI.as_view(), name='update_stock_api'),

    # path('category/<slug:slug>/', ProductByCategoryView.as_view(), name='products_by_category'),
    #  path('category/<int:category_id>/', ProductByCategoryView.as_view(), name='products_by_category'),
]
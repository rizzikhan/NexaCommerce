from django.urls import path
from . import views
from .views import *



app_name="display"

urlpatterns = [
    path('dashboard/', views.display, name='display'), #for displaying all products to merchant and user 
    path('api/products/', ProductSearchAPIView.as_view(), name='product-search'),# for search
    path("api/products/add/", AddProductAPIView.as_view(), name="add_product"),# for adding product 
    path('api/products/<int:pk>/update', ProductDetailAPIView.as_view(), name='product-detail'),#can be used for FETCH UPDATE DELETE  # this for updating merchant product 
    path('api/products/<int:pk>/delete', DeleteProductAPIView.as_view(), name='delete-product'),  # for deleting mercahnt product 
    path('api/merchant-products/', MerchantProductsAPIView.as_view(), name='merchant-products'),# merchant product refreshing after delete update and new product 


    path("watchlist/", toggle_watchlist, name="toggle-watchlist"),  # Watchlist toggle endpoint
    path("api/watchlist/", get_watchlist, name="get-watchlist"),

    path('api/products/<int:pk>/detailpage', detailedpage, name='detailedpage'), # 

    path('products/<int:pk>/comments/', fetch_comments, name='fetch-comments'),#fetch comments
    path('products/<int:pk>/add-comment/', add_comment, name='add-comment'), # add comments

    path('about/', views.about_us, name='about_us'),


]

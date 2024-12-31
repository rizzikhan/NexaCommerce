from django.urls import path
from .views import CartAPIView
from . import views
from .views import CreateCheckoutSessionAPIView  , CheckoutCancelView , OrderDoneListView ,orders_template_view 


app_name = "cart"
urlpatterns = [
    path('', CartAPIView.as_view(), name='cart-api'),  # For GET and POST for Cart items
    path('<int:pk>/', CartAPIView.as_view(), name='cart-item-api'),  # For DELETE Cart Items
    path("checkout/", views.checkout_view, name="checkout"),
 
    
    path("create-checkout-session/", CreateCheckoutSessionAPIView, name="create-checkout-session"), 
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),

    path('checkout/success/', views.checkout_success, name='checkout-success'),
    path("checkout/cancel/", CheckoutCancelView.as_view(), name="checkout-cancel"),



    path('orders/', OrderDoneListView.as_view(), name='order-done-list'),
    path('orders/view/', orders_template_view, name='order-done-template'), 


    path('refund/', views.process_refund, name='process-refund'), #refund API 

    path('add/', CartAPIView.as_view(), name='addtocart'),  # Merchant post product 


]

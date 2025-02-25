from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from .models import Cart ,ProductSales
from .serializers import CartSerializer
from display.models import Product 
from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseBadRequest
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import OrderDone, Cart  
from userauth.models import CustomUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from django.http import JsonResponse
import json



class CartAPIView(APIView):
    # For getting cart items of a specific user
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        print(f"Cart items for user {request.user}: {cart_items}")
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # For adding to cart
    def post(self, request):
        product_id = request.data.get("product_id")
        try:
            print("We are in POST of CartAPIView in cart app")
            quantity = int(request.data.get("quantity", 1))
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid quantity provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not product_id:
            return Response(
                {"error": "Product ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if quantity > product.stock:
            return Response(
                {"error": "Quantity exceeds available stock"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            if cart_item.quantity + quantity > product.stock:
                return Response(
                    {"error": "Total quantity in cart exceeds available stock"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            cart_item.quantity += quantity

        cart_item.save()
        print(f"Cart item created: {created}, Quantity: {cart_item.quantity}")
        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)

        

#for removing item from cart Remove button 
    def delete(self, request, pk):
        try:
            cart_item = Cart.objects.get(id=pk, user=request.user)
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)






@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "total_quantity": total_quantity,
    }
    return render(request, "cart/checkout.html", context)


@login_required
def update_cart_quantity(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cart_item_id = data.get("cart_item_id")
            quantity = int(data.get("quantity", 1))

            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            if quantity <= 0 or quantity > cart_item.product.stock:
                return JsonResponse({"error": "Invalid quantity or exceeds stock"}, status=400)
            
            cart_item.quantity = quantity
            cart_item.save()

            total_quantity = sum(item.quantity for item in Cart.objects.filter(user=request.user))
            total_price = sum(item.product.price * item.quantity for item in Cart.objects.filter(user=request.user))

            return JsonResponse({
                "subtotal": cart_item.product.price * quantity,
                "total_quantity": total_quantity,
                "total_price": total_price
            })

        except Cart.DoesNotExist:
            return JsonResponse({"error": "Cart item not found"}, status=404)
        except ValueError:
            return JsonResponse({"error": "Invalid quantity value"}, status=400)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateCheckoutSessionAPIView(request):
    print("we are in create CHeckout sessions API view ")
    user_cart = Cart.objects.filter(user=request.user)
    
    if not user_cart.exists():
        return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        line_items = []
        total_amount = 0
        
        for cart_item in user_cart:
            if not cart_item.product or cart_item.product.price is None:
                print(f"Skipping cart item {cart_item.id} - invalid product")
                continue
            
            item_total = cart_item.product.price * cart_item.quantity
            total_amount += item_total
            
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": cart_item.product.name,
                    },
                    "unit_amount": int(cart_item.product.price * 100),
                },
                "quantity": cart_item.quantity,
            })
        
        if not line_items:
            return Response({"error": "No valid items in the cart."}, status=status.HTTP_400_BAD_REQUEST)
        
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            metadata={
                'user_id': str(request.user.id),
                'order_type': 'cart_checkout'
            },
            success_url=f"http://127.0.0.1:8000/api/cart/checkout/success/",
            cancel_url="http://127.0.0.1:8000/api/cart/checkout/cancel/",
        )
        print(f"session id is createcheckoutsessionapiview {session.id}")

        return Response({"sessionId": session.id})
    
    except stripe.error.StripeError as e:
        return Response({"error": str(e)}, status=status.HTTP_402_PAYMENT_REQUIRED)
    except Exception as e:
        print(f"Unexpected error in checkout: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


def send_order_receipt(user_email, products, total_amount ,order_id):
    subject = 'Your Order Receipt'
    from_email = settings.EMAIL_HOST_USER
    to = [user_email]
    
    context = {
        'cart_items': products,
        'order_total': total_amount,
        'current_year': datetime.now().year,
        'order_id':order_id
    }
    
    html_content = render_to_string('cart/order_receipt.html', context)
    text_content = f"Thank you for your order! Your order ID is.{order_id} Total: ${total_amount}"
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print("Order receipt email sent successfully")
    

def send_order_cancellation_email(user_email, products, total_amount, order_id):
    subject = 'Your Order Cancellation Confirmation'
    from_email = settings.EMAIL_HOST_USER
    to = [user_email]
    
    context = {
        'cart_items': products,
        'order_total': total_amount,
        'current_year': datetime.now().year,
        'order_id': order_id
    }
    
    html_content = render_to_string('cart/order_cancellation.html', context)
    text_content = f"Your order with ID {order_id} has been successfully cancelled. Total amount: ${total_amount}."
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print("Order cancellation confirmation email sent successfully")


@csrf_exempt
def stripe_webhook(request):
    print("we are in stripe webhook")

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    print(f"Signature Header: {sig_header}")
    print(f"Webhook Secret: {endpoint_secret}")

    if not sig_header:
        print("Missing Stripe Signature Header")
        return HttpResponseBadRequest("Missing signature header")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        print("Invalid payload")
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError:
        print("Invalid signature")
        return HttpResponseBadRequest("Invalid signature")

    if event['type'] == 'checkout.session.completed':
        print("we are in the IF of session completed ")
        print(f"event['type']: {event['type']}")
        session = event['data']['object']

        print(f"Payment successful for session {session['id']}")
        print("Webhook Triggered: checkout.session.completed")
        user_id = session.get('metadata', {}).get('user_id')
        payment_intent_id = session.get('payment_intent')
        print(f"intent: {payment_intent_id}")

        print("userid:", user_id)
        if not user_id:
            print("User ID not found in metadata")
            return HttpResponseBadRequest("Missing user ID")

        try:
            user = CustomUser.objects.get(id=user_id)
            print("fetching user using userid:", user)

            cart_items = Cart.objects.filter(user=user)
            if not cart_items.exists():
                print("No cart items found for this user")
                return HttpResponseBadRequest("No cart items found")

            products = []
            total_amount = 0
            for item in cart_items:
                products.append({
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "price": float(item.product.price)
                })
                total_amount += float(item.product.price) * item.quantity

                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()
                    print(f"Stock updated for product {item.product.name}, new stock: {item.product.stock}")
                else:
                    print(f"Insufficient stock for product {item.product.name}")
                    return HttpResponseBadRequest(f"Insufficient stock for product {item.product.name}")
                
            
                        # Update sales count
                product_sales, created = ProductSales.objects.get_or_create(product=item.product)
                product_sales.sales_count += item.quantity
                product_sales.save()
                print(f"Sales count updated for product {item.product.name}, new count: {product_sales.sales_count}")


            print(f"user: {user}")
            print(f"products: {products}")
            print(f"total_amount: {total_amount}")
            print(f"stripe_session_id: {session['id']}")

            order = OrderDone.objects.create(
                user=user,
                products=products,
                total_amount=total_amount,
                stripe_session_id=session['id'],
                intent=payment_intent_id,
            )
            order_id = order.order_id

            print(f"user: {user}")
            print(f"order_id: {order_id}")
            print(f"products: {products}")
            print(f"total_amount: {total_amount}")
            print(f"stripe_session_id: {session['id']}")
            print(f"intent: {payment_intent_id}")

            try:
                send_order_receipt(user.email, products, total_amount, order_id)
                print("Email sent successfully")
            except Exception as email_error:
                print(f"Failed to send email: {email_error}")
                return HttpResponseBadRequest("Failed to send order email")

            cart_items.delete()

            print(f"Order saved and cart cleared for user {user.username}")

        except Exception as e:
            print(f"Error saving order: {e}")
            return HttpResponseBadRequest("Error processing order")

    if event['type'] in ['charge.refunded', 'charge.refund.updated']:
        print("Webhook Triggered: charge.refunded or charge.refund.updated")

        charge = event['data']['object']
        payment_intent_id = charge.get('payment_intent')

        print(f"Refund event received for Payment Intent: {payment_intent_id}")

        try:
            order = OrderDone.objects.get(intent=payment_intent_id)
            order_id = order.order_id

            order.refund_status = "Refunded"
            order.is_refunded = True
            order.save()
            print(f"Refund status updated for order {order_id}")

            try:
                send_order_cancellation_email(order.user.email, order.products, order.total_amount, order_id)
                print("Cancellation confirmation email sent successfully")
            except Exception as email_error:
                print(f"Failed to send cancellation email: {email_error}")
                return HttpResponseBadRequest("Failed to send cancellation email")
        except OrderDone.DoesNotExist:
            print(f"No order found for intent {payment_intent_id}")

    return HttpResponse(status=200)


def checkout_success(request):
    return render(request, 'cart/checkout_success.html')


class CheckoutCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Checkout was canceled. Your cart is still intact."})


class OrderDoneListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = OrderDone.objects.filter(user=request.user)  
        order_list = []

        for order in orders:
            order_list.append({
                "id": order.id,
                "total_amount": order.total_amount,
                "created_at": order.created_at,
                "products": order.products,  
                "intent": order.intent,  
                "refund_status": order.refund_status,  
                "is_refunded": order.is_refunded,  

            })

        return Response({"orders": order_list})
    

@login_required
def orders_template_view(request):
    orders = OrderDone.objects.filter(user=request.user) 
    return render(request, "cart/orders.html", {"orders": orders})



@csrf_exempt
@api_view(['POST'])
def process_refund(request):
    order_id = request.data.get('order_id')
    intent_id = request.data.get('intent_id')
    print("we are in process_refund")
    try:
        # Fetch the order
        order = OrderDone.objects.get(id=order_id, intent=intent_id)
        print(f"Order list: {order}")

        # Process refund via Stripe
        refund = stripe.Refund.create(payment_intent=intent_id)
        print("Going to refund user")
        
        # Update refund status
        order.refund_status = "Refunded"
        order.is_refunded = True
        order.save()

        # Iterate through products in the order
        for item in order.products:  # Assuming `products` is a JSON field
            product = Product.objects.get(name=item['name'])  # Match by name or ID
            
            # Adjust stock (add refunded quantity back to stock)
            product.stock += item['quantity']
            product.save()
            print(f"Stock restored for product {product.name}, new stock: {product.stock}")

            # Adjust sales and return counts
            product_sales, created = ProductSales.objects.get_or_create(product=product)
            product_sales.sales_count = max(product_sales.sales_count - item['quantity'], 0)
            product_sales.return_count += item['quantity']  # Increment return count
            product_sales.save()

            print(f"Updated sales and return counts for product {product.name}")

        return Response({"message": "Refund processed successfully."})

    except OrderDone.DoesNotExist:
        print("Order not found")
        return Response({"error": "Order not found."}, status=404)
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        print(f"Unexpected error during refund: {e}")
        return Response({"error": "An error occurred while processing the refund."}, status=500)

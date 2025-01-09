from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer ,CategorySerializer
from django.db.models import Q
from django.shortcuts import render, get_object_or_404 
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Product, Comment, Watchlist ,Category
from django.http import JsonResponse
from django.shortcuts import render 
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from .models import CarouselImage
from django.db.models import Sum


# for displaying display of all products and merchant products 
def display(request):
    products = Product.objects.all()
    print(products)
    print("Fetching products in display")
    
    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    start_url = f'{protocol}://{current_site.domain}'
    
    if request.user.is_authenticated:
        user_watchlist = Watchlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        user_watchlist = []  

    for product in products:
        product.in_watchlist = product.id in user_watchlist
        print(f"product.in_watchlist {product.in_watchlist}")
        
    merchant_products = None
    if request.user.is_authenticated and request.user.role == 'merchant':
        merchant_products = Product.objects.filter(merchant=request.user)
        print(f"Merchant products for {request.user}: {merchant_products}")

        return render(request, 'display/index.html', {
        'merchant_products': merchant_products,
    })
    else:
        return render(request, 'display/index.html', {
        'products': products,
        'start_url': start_url
    })




def home(request):
    # Fetch the categories "Sale Items" and "Discounted"
    sale_category = Category.objects.filter(name="Sale Items").first()
    discounted_category = Category.objects.filter(name="Discounted").first()
    carousel_images = CarouselImage.objects.filter(is_active=True)

    # Get products from the respective categories
    sale_products = Product.objects.filter(category=sale_category) if sale_category else []
    discounted_products = Product.objects.filter(category=discounted_category) if discounted_category else []

        # Fetch top 5 most selling products
    top_selling_products = (
        Product.objects.annotate(total_sales=Sum('sales_data__sales_count'))
        .order_by('-total_sales')[:5]
    )

    # Context for the template
    context = {
        'carousel_images': carousel_images,
        'sale_products': sale_products,
        'discounted_products': discounted_products,
        'top_selling_products': top_selling_products,

    }
    
    return render(request, 'display/home.html', context)


def product_list(request):
    products = Product.objects.all()

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category = request.GET.get('category')
    in_stock = request.GET.get('in_stock')
    sort_by = request.GET.get('sort')

    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    if category:
        products = products.filter(category__id=category)
    if in_stock == 'true':
        products = products.filter(stock__gt=0)

    sort_options = {
        'price_low_high': 'price',
        'price_high_low': '-price',
        'new_to_old': '-created_at',
        'old_to_new': 'created_at'
    }
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])

    product_data = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'category': product.category.name if product.category else 'Uncategorized',
            'stock': product.stock,
            'image': product.image.url if product.image else None,
            'in_watchlist': False  
        }
        for product in products
    ]
    return JsonResponse({'products': product_data})



def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'display/category_products.html', {'category': category, 'products': products})


class ProductSearchAPIView(APIView):
    def get(self, request):
        search_query = request.GET.get('search')  
        if search_query:
            products = Product.objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(price__icontains=search_query) 
            )
        else:
            products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(merchant=self.request.user)
    

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        print(f"categories {categories}")
        serializer = CategorySerializer(categories, many=True)
        print(f"serializer.data{serializer.data}")
        return Response(serializer.data)

class AddProductAPIView(APIView):
    def post(self, request):
        print("add product API called")
        
        category_id = request.data.get("category")

        if not category_id:
            return Response({"error": "Category is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Invalid category selected"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductSerializer(data=request.data, context={"request": request})  

        if serializer.is_valid():
            product = serializer.save(category=category) 
            return Response({"product": ProductSerializer(product).data}, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

class DeleteProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk, merchant=request.user)
            product.delete()  
            return Response({"message": "Product deleted successfully."}, status=204)  
        except Product.DoesNotExist:
            return Response({"error": "Product not found or permission denied."}, status=404)


class MerchantProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        merchant_products = Product.objects.filter(merchant=request.user)
        serializer = ProductSerializer(merchant_products, many=True)
        return Response(serializer.data)
    


@api_view(['POST'])
def toggle_watchlist(request):
    product_id = request.data.get("product_id")
    print(f"we are in toggle watchlist {product_id}")
    if not product_id:
        print(f"no prodcut id  {product_id}")
        return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id)
        
        watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, product=product)
        print(f"watchlist_item  {watchlist_item}")
        print(f"created {created}")

        if created:
            return Response({
                "message": "Added to watchlist.",
                "in_watchlist": True
            }, status=status.HTTP_201_CREATED)
        else:
            watchlist_item.delete()
            return Response({
                "message": "Removed from watchlist.",
                "in_watchlist": False
            }, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def get_watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    data = [
        {
            "id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "product_price": item.product.price,
            "product_image": item.product.image.url if item.product.image else None,
        }
        for item in watchlist_items
    ]
    return Response({"watchlist": data}, status=status.HTTP_200_OK)




def detailedpage(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print(f"product.category{product.category}")
    specific_category = product.category
    suggested_products = Product.objects.filter(category=specific_category).exclude(pk=pk)
    print(f"specific_products{suggested_products}")
    comments = product.comments.all()
    
    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    absolute_url = f'{protocol}://{current_site.domain}{product.get_absolute_url()}'
    
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        rating = request.POST.get("rating", 0)
        if comment_text and rating:
            Comment.objects.create(user=request.user, product=product, comment_text=comment_text, rating=rating)

    print(f"absolute_url{absolute_url}")

    context = {
        'product': product,
        'comments': comments,
        'absolute_url': absolute_url,
        'suggested_products':suggested_products ,
    }
    
    return render(request, 'display/detailpage.html', context)


def load_comments(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = product.comments.all().order_by('-created_at')
    comments_data = [
        {
            'user': comment.user.username,
            'comment_text': comment.comment_text,
            'rating': comment.rating,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for comment in comments
    ]
    return JsonResponse({'comments': comments_data})


@api_view(['POST'])
def add_comment(request, pk):

    product = Product.objects.get(pk=pk)
    comment_text = request.data.get('comment')
    rating = request.data.get('rating', 0)

    if not comment_text:
        return Response({"error": "Comment text is required"}, status=status.HTTP_400_BAD_REQUEST)

    Comment.objects.create(
        user=request.user,
        product=product,
        comment=comment_text,
        rating=rating,
    )

    return Response({}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def fetch_comments(request, pk):

    product = Product.objects.get(pk=pk)
    comments = product.comments.all().order_by('-created_at')
    data = [
        {
            "user": comment.user.username,
            "comment": comment.comment,
            "rating": comment.rating,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for comment in comments
    ]
    return Response(data, status=status.HTTP_200_OK)



def about_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(
            f'Contact Form Submission from {name}',
            message,
            email,
            ['rizwanpiecyfer@gmail.com'],  
        )
        print("email sent ")
        return JsonResponse({'message': 'Thank you for your message! We will get back to you soon.'})
    
    return render(request, 'display/about_us.html')



def product_detail_url(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


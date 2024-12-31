
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from django.db.models import Q
from django.shortcuts import render, get_object_or_404 
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Product, Comment, Watchlist 
from django.http import JsonResponse
from django.shortcuts import render 
from django.http import JsonResponse
from django.core.mail import send_mail


# for displaying display of all products and merchant products 
def display(request):
    products = Product.objects.all()
    print(products)
    print("Fetching products in display")

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
    })



#searchAPI
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


# for updating merchant added product 
class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(merchant=self.request.user)
    

    #for adding a new product
class AddProductAPIView(APIView):
    def post(self, request):
        print("add product API called")
        serializer = ProductSerializer(data=request.data, context={"request": request})  

        if serializer.is_valid():
            product = serializer.save() 
            return Response({"product": ProductSerializer(product).data}, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

#for deleting merchant product
class DeleteProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk, merchant=request.user)
            product.delete()  
            return Response({"message": "Product deleted successfully."}, status=204)  
        except Product.DoesNotExist:
            return Response({"error": "Product not found or permission denied."}, status=404)


#for refreshing merchant products after updation/deletion
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
    comments = product.comments.all()  
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        rating = request.POST.get("rating", 0)
        if comment_text and rating:
            Comment.objects.create(user=request.user, product=product, comment_text=comment_text, rating=rating)

    return render(request, 'display/detailpage.html', {
        'product': product,
        'comments': comments,
    })


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






# def upload_pdf(request):
#     if request.method == 'POST':
#         pdf_file = request.FILES.get('pdf_file')
#         if pdf_file:
#             document = Document.objects.create(name=pdf_file.name, pdf_file=pdf_file)
#             return redirect('display:process_pdf', document_id=document.id)
#     return render(request, 'display/upload.html')


# def process_pdf_view(request, document_id):
#     document = Document.objects.get(id=document_id)
#     file_path = document.pdf_file.path
    
#     try:
#         process_pdf(file_path)
#         document.processed = True
#         document.save()
#         return JsonResponse({'status': 'success', 'message': 'PDF processed successfully.'})
#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)})


import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai.llms import GoogleGenerativeAI
from display.models import Watchlist, Comment , Product
from cart.models import Cart,OrderDone ,ProductSales
from django.utils.html import format_html


# Process PDF into FAISS
def process_pdf(file_path):
    text = ''
    pdf_reader = PdfReader(file_path)
    for page in pdf_reader.pages:
        text += page.extract_text() or ''
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    
    os.makedirs('shared_storage/vectorstore', exist_ok=True)
    vector_store.save_local('shared_storage/vectorstore/faiss_index')

# Load FAISS index
def load_static_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    return FAISS.load_local(
        folder_path='shared_storage/vectorstore/faiss_index',
        embeddings=embeddings,
        allow_dangerous_deserialization=True 
    )

def get_dynamic_user_data(user):

    if not user.is_authenticated:
        return format_html("<b>⚠️ You need to be logged in to view personalized data.</b>")

    cart_items = Cart.objects.filter(user=user)
    orders = OrderDone.objects.filter(user=user).order_by('-created_at')  
    watchlist = Watchlist.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)
    product_sales = ProductSales.objects.all()

    # 🛒 Cart Items
    cart_data = "".join([
        f"• <b>{item.product.name}</b> (Qty: {item.quantity})<br>"
        for item in cart_items
    ]) if cart_items.exists() else "<i>No items in cart.</i>"

    # 📦 Orders with Refund Status
    order_data = ""
    for order in orders:
        product_details = ""
        for product in order.products:
            product_name = product.get('name', 'Unknown Product')
            quantity = product.get('quantity', 1)
            product_details += f"    • {product_name} (Qty: {quantity})<br>"

        # Check for refund status
        refund_info = f"<b>Refund Status:</b> {order.refund_status}<br>" if order.is_refunded else "<b>Refund Status:</b> Not Refunded<br>"

        order_data += (
            f"<b>Order ID:</b> {order.order_id}<br>"
            f"{product_details}"
            f"<b>Total:</b> ${order.total_amount}<br>"
            f"{refund_info}<br>"
        )

    order_data = order_data or "<i>No orders placed.</i>"

    # 🛍️ Product Details
    product_data = "".join([
        f"<b>{product.name}</b><br>"
        f"📄 Description: {product.description}<br>"
        f"💲 Price: ${product.price}<br>"
        f"📦 Stock: {product.stock} available<br><br>"
        for product in Product.objects.all()
    ]) or "<i>No product data available.</i>"

    # 👀 Watchlist
    watchlist_data = "".join([
        f"• <b>{item.product.name}</b><br>"
        for item in watchlist
    ]) or "<i>No items in watchlist.</i>"

    # 💬 Comments
    comment_data = "".join([
        f"• <b>{comment.product.name}</b>: \"{comment.comment}\"<br>"
        for comment in comments
    ]) or "<i>No comments yet.</i>"

    # 📊 Product Sales Data
    sales_data = "".join([
        f"• <b>{sale.product.name}</b>: Sold <b>{sale.sales_count}</b>, Returned <b>{sale.return_count}</b><br>"
        for sale in product_sales
    ]) or "<i>No product sales data available.</i>"

    # 📋 Final Combined Response
    user_data = format_html(f"""
    <h3>🛒 <u>Your Cart:</u></h3>
    {cart_data}<br>

    <h3>📦 <u>Your Orders:</u></h3>
    {order_data}<br>

    <h3>🛍️ <u>Available Products:</u></h3>
    {product_data}

    <h3>👀 <u>Your Watchlist:</u></h3>
    {watchlist_data}<br>

    <h3>💬 <u>Your Comments:</u></h3>
    {comment_data}<br>

    <h3>📊 <u>Product Sales Data:</u></h3>
    {sales_data}
    """)

    return user_data




# Combine dynamic and static data
def combine_data(user_query, user):
    static_store = load_static_vector_store()
    static_docs = static_store.similarity_search(user_query, k=3)
    static_data = "\n".join([doc.page_content for doc in static_docs])

    dynamic_data = get_dynamic_user_data(user)

    return f"User Data:\n{dynamic_data}\n\nCompany Policies:\n{static_data}"

# Query combined data and user question processing 
def query_combined_data(user_query, user):
    try:
        context = combine_data(user_query, user) #static and dynamic data coming from db 
        llm = GoogleGenerativeAI(model="gemini-1.5-flash")
        prompt = f"Context:\n{context}\n\nUser Question: {user_query}\nAnswer:"
        return llm.predict(prompt)
    except Exception as e:
        return f"Error: {e}"

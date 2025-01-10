from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Document
from .utils import process_pdf, query_vector_store
from django_ratelimit.decorators import ratelimit


def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            document = Document.objects.create(name=pdf_file.name, pdf_file=pdf_file)
            return redirect('process_pdf', document_id=document.id)
    return render(request, 'chatbot/upload.html')


def process_pdf_view(request, document_id):
    document = Document.objects.get(id=document_id)
    file_path = document.pdf_file.path
    
    try:
        process_pdf(file_path)
        document.processed = True
        document.save()
        return JsonResponse({'status': 'success', 'message': 'PDF processed successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def chatbot_view(request):
    return render(request, 'chatbot/chat.html')


FORBIDDEN_WORDS = ['attack', 'hack', 'malware']

def contains_prohibited_content(query):
    return any(word in query.lower() for word in FORBIDDEN_WORDS)



@ratelimit(key='ip', rate='10/m', block=True)  # Limit to 10 requests per minute per IP
def process_query(request):
    if request.method == 'POST':
        user_query = request.POST.get('question')   
        if contains_prohibited_content(user_query):
            return JsonResponse({'response': 'Your query contains prohibited content.'}, status=400)

        if user_query:
            response = query_vector_store(user_query)
            return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)

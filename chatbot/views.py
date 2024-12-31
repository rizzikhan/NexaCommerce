from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Document
from .utils import process_pdf, query_vector_store

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


def process_query(request):
    if request.method == 'POST':
        user_query = request.POST.get('question')
        if user_query:
            response = query_vector_store(user_query)
            return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Document
from .utils import process_pdf, query_combined_data
from django_ratelimit.decorators import ratelimit
from .models import ChatHistory

def chatbot_view(request):
    if request.user.is_authenticated:
        chat_history = ChatHistory.objects.filter(user=request.user).order_by('timestamp')
    else:
        chat_history = None

    return render(request, 'chatbot/chat.html', {'chat_history': chat_history})


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




@ratelimit(key='ip', rate='10/m', block=True)
def process_query(request):
    if request.method == 'POST':
        user_query = request.POST.get('question')

        if not request.user.is_authenticated:
            return JsonResponse({'response': "⚠️ Please log in to access your personal data."})

        if user_query:
            response = query_combined_data(user_query, request.user)

            ChatHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                user_message=user_query,
                bot_response=response
            )
            return JsonResponse({'response': str(response)})

    return JsonResponse({'error': 'Invalid request'}, status=400)


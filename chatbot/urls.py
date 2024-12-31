from django.urls import path
from . import views


app_name = "chatbot"
urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('process/<int:document_id>/', views.process_pdf_view, name='process_pdf'),
    path('chat/', views.chatbot_view, name='chatbot'),
    path('process_query/', views.process_query, name='process_query'),
]

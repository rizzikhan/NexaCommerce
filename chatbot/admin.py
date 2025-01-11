from django.contrib import admin
from .models import Document ,ChatHistory
from .utils import process_pdf
from django.contrib import messages

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'processed', 'created_at')
    list_filter = ('processed', 'created_at')
    actions = ['process_selected_pdfs']

    def process_selected_pdfs(self, request, queryset):
 
        for document in queryset:
            if not document.processed:
                try:
                    process_pdf(document.pdf_file.path)
                    document.processed = True
                    document.save()
                    self.message_user(request, f"Processed {document.name} successfully.", messages.SUCCESS)
                except Exception as e:
                    self.message_user(request, f"Failed to process {document.name}: {e}", messages.ERROR)
            else:
                self.message_user(request, f"{document.name} is already processed.", messages.WARNING)

    process_selected_pdfs.short_description = "Process selected PDFs and generate FAISS indexes"





@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_message', 'bot_response', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username', 'user_message', 'bot_response')
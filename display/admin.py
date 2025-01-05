from django.contrib import admin
from .models import Product , Watchlist , Comment , Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',  'description','price','stock', 'merchant' ,'created_at','updated_at','category')
    list_filter = ('stock', 'price','merchant','category')
    search_fields = ('name','description','stock')
    readonly_fields = ('created_at', 'updated_at')
    list_display_links = ["name","description"]
    list_editable = ('price', 'stock')
    actions = []
    list_per_page = 20
    empty_value_display = "-empty-" 


    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'stock', 'image', 'merchant')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(merchant=request.user)

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')  
    list_filter = ('user', 'added_at')  
    search_fields = ('user__username', 'product__name') 
    ordering = ('-added_at',)  
    readonly_fields = ('added_at',)
    actions = ['clear_watchlist']

    def clear_watchlist(self, request, queryset):
        
        count = queryset.delete()
        self.message_user(request, f"Successfully cleared {count[0]} watchlist items.")

    clear_watchlist.short_description = "Clear selected watchlist items"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass








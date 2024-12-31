from django.contrib import admin
from .models import Cart, OrderDone

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    list_filter = ('user', 'added_at')
    search_fields = ('user__username', 'product__name')
    ordering = ('-added_at',)
    readonly_fields = ('added_at',)

    actions = ['clear_cart']

    def clear_cart(self, request, queryset):
   
        count = queryset.delete()
        self.message_user(request, f"Successfully cleared {count[0]} cart items.")

    clear_cart.short_description = "Clear selected cart items"

@admin.register(OrderDone)
class OrderDoneAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'refund_status', 'is_refunded', 'created_at', 'intent')
    list_filter = ('user', 'is_refunded', 'refund_status', 'created_at')
    search_fields = ('user__username', 'products', 'stripe_session_id', 'intent')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'stripe_session_id', 'intent')

    actions = ['mark_as_refunded', 'mark_as_not_refunded']

    def mark_as_refunded(self, request, queryset):

        count = queryset.update(refund_status="Refunded", is_refunded=True)
        self.message_user(request, f"Successfully marked {count} orders as refunded.")

    mark_as_refunded.short_description = "Mark selected orders as refunded"

    def mark_as_not_refunded(self, request, queryset):

        count = queryset.update(refund_status="Not Refunded", is_refunded=False)
        self.message_user(request, f"Successfully marked {count} orders as not refunded.")

    mark_as_not_refunded.short_description = "Mark selected orders as not refunded"

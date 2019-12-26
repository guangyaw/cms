from django.contrib import admin
from coins.models import TradeRecord, BestValues, PreOrder


class TradeRecordAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'side', 'quantity', 'price', 'fee', 'timestamp')
    list_filter = ("symbol",)
    search_fields = ("symbol", "timestamp")
    ordering = ("-timestamp", "symbol")


class BestValuesAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'best_price', 'best_bid', 'best_ask', 'timestamp')
    list_filter = ("symbol",)
    search_fields = ("symbol", "timestamp")
    ordering = ("-timestamp", "symbol")


class PreOrderAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'stop_point', 'base_amount', 'end_amount', 'status', 'timestamp')
    list_filter = ("symbol",)
    search_fields = ("symbol", "timestamp")
    ordering = ("-timestamp", "status")


admin.site.register(BestValues, BestValuesAdmin)
admin.site.register(PreOrder, PreOrderAdmin)
admin.site.register(TradeRecord, TradeRecordAdmin)

from django.contrib import admin
from coins.models import TradeRecord, BestValues


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


admin.site.register(BestValues, BestValuesAdmin)
admin.site.register(TradeRecord, TradeRecordAdmin)

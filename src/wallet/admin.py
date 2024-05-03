from django.contrib import admin
from django.http import HttpRequest
from src.wallet.models import Wallet, WalletTransaction
from typing import Any


class WalletTransactionAdmin(admin.ModelAdmin):
    readonly_fields = ("change_amount",)


class WalletTransactionTabular(admin.TabularInline):
    model = WalletTransaction
    extra = 0
    fields = ("wallet", "action", "change_amount", "currency", "created_at")
    readonly_fields = ("wallet", "action", "change_amount", "currency", "created_at")
    ordering = ("-created_at",)

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return False

    def has_add_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False


class WalletAdmin(admin.ModelAdmin):
    inlines = (WalletTransactionTabular,)


admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)

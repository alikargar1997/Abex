from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ExchangeTypes(TextChoices):
    BUY = "buy", _("Buy")
    SELL = "sell", _("Sell")


class SettlementStatuses(TextChoices):
    CREATED = "created", _("Created")
    PENDING = "pending", _("Pending")
    DONE = "done", _("Done")
    FAILED = "failed", _("Failed")

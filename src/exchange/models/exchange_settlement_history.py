from django.db import models
from src.core.utils.model import BaseTimestampedModel
from src.exchange.models import Exchange
from src.exchange.const import SettlementStatuses


class ExchangeSettlementHistory(BaseTimestampedModel):
    updated_at = None
    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name="settlement_histories",
    )
    status = models.CharField(
        max_length=10, choices=SettlementStatuses.choices
    )
    status_code = models.PositiveIntegerField()
    response = models.TextField(null=True)

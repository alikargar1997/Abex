from django.db import models
from django.conf import settings
from src.core.utils.model import BaseTimestampedModel
from src.core.const import MoneyCurrencies
from src.exchange.const import ExchangeTypes, SettlementStatuses
from django.db.models import F, Sum, Subquery, OuterRef


class ExchangeCustomQuerySet(models.QuerySet):
    def exchanges_to_settle(
        self, cryptocurrency_title: str
    ) -> models.QuerySet:
        return self.filter(
            settlement_status=SettlementStatuses.CREATED,
            exchange_type=ExchangeTypes.BUY,
            cryptocurrency__title=cryptocurrency_title,
        )


class ExchangeCustomManager(models.Manager):
    def get_queryset(self) -> ExchangeCustomQuerySet:
        return ExchangeCustomQuerySet(self.model, using=self._db).select_related(
            "cryptocurrency"
        )

    def get_exchanges_to_settle(
        self, cryptocurrency_title: str
    ) -> models.QuerySet:
        return self.get_queryset().exchanges_to_settle(
            cryptocurrency_title
        )


class Exchange(BaseTimestampedModel):
    """
    Represents an exchange transaction for a cryptocurrency.

    Attributes:
        user (django.contrib.auth.models.User): The user who performed the exchange.
        cryptocurrency (cryptocurrency.models.Cryptocurrency): The cryptocurrency involved in the exchange.
        quantity (int): The quantity of the cryptocurrency exchanged.
        exchange_type (str): The type of exchange, either "BUY" or "SELL".
        unit_price_amount (decimal.Decimal): The price per unit of the cryptocurrency.
        currency (str): The currency used for the exchange, typically "USD".
        wallet_transaction (wallet.models.WalletTransaction): The wallet transaction associated with the exchange.

    Properties:
        total_price_amount (float): The total price of the exchange, calculated as the unit price multiplied by the quantity.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="exchanges"
    )
    cryptocurrency = models.ForeignKey(
        "cryptocurrency.Cryptocurrency",
        on_delete=models.PROTECT,
        related_name="users_exchanges",
    )
    quantity = models.PositiveBigIntegerField()
    exchange_type = models.CharField(
        max_length=5, choices=ExchangeTypes.choices, default=ExchangeTypes.BUY
    )
    unit_price_amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(
        max_length=5, choices=MoneyCurrencies.choices, default=MoneyCurrencies.USD
    )
    wallet_transaction = models.ForeignKey(
        "wallet.WalletTransaction", on_delete=models.PROTECT, related_name="exchanges"
    )
    settlement_status = models.CharField(
        max_length=10,
        choices=SettlementStatuses.choices,
        default=SettlementStatuses.CREATED,
    )
    objects = models.Manager()
    custom_objects = ExchangeCustomManager()

    @property
    def total_price_amount(self) -> float:
        return self.unit_price_amount * self.quantity

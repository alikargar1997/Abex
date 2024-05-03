from django.db import models
from django.conf import settings
from src.core.utils.model import BaseTimestampedModel
from src.core.const import MoneyCurrencies


class WalletCustomManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related("user")


class Wallet(BaseTimestampedModel):
    """
    Represents a user's wallet, which holds their account balance and currency.

    Attributes:
        wallet (auth.User): Is a one-to-one relationship with the Django `User` model, meaning each user has a single wallet associated with their account.
        balance_amount (Decimal): Stores the user's current account balance
        currency (str): The currency of the transaction, such as USD.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="wallet"
    )
    balance_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    currency = models.CharField(
        max_length=5, default=MoneyCurrencies.USD, choices=MoneyCurrencies.choices
    )
    objects = models.Manager()
    custom_objects = WalletCustomManager()

    def __str__(self) -> str:
        return self.user.username

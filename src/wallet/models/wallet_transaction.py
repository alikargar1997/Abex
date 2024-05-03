from django.db import models
from src.core.utils.model import BaseTimestampedModel
from src.core.const import MoneyCurrencies
from src.wallet.const import WalletActionType


class WalletTransaction(BaseTimestampedModel):
    """
    Represents record of a transaction made to a user's wallet.

    Attributes:
        wallet (wallet.Wallet): The wallet that the transaction was made to.
        action (str): The type of action performed on the wallet, such as a withdrawal or deposit.
        change_amount (Decimal): The amount of money that was added or removed from the wallet.
        currency (str): The currency of the transaction, such as USD.
    """

    updated_at = None
    wallet = models.ForeignKey(
        "wallet.Wallet", on_delete=models.PROTECT, related_name="transactions"
    )
    action = models.CharField(
        max_length=10,
        choices=WalletActionType.choices,
        default=WalletActionType.WITHDRAW,
    )
    change_amount = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    currency = models.CharField(
        max_length=5, default=MoneyCurrencies.USD, choices=MoneyCurrencies.choices
    )

    def __str__(self) -> str:
        return f"{self.wallet.user} - {self.action}"

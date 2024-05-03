from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class WalletActionType(TextChoices):
    DEPOSIT = "deposit", _("Deposit")
    WITHDRAW = "withdraw", _("Withdraw")

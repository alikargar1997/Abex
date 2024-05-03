from django.db import models
from solo.models import SingletonModel
from django.utils.translation import gettext_lazy as _
from src.abex_settings.const import SettleStrategies


class AbexSettings(SingletonModel):
    min_amount_intl_exchanges_support = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=10.0,
        help_text=_("Minimum amount supported by international exchanges."),
    )
    settle_strategy = models.CharField(
        max_length=10,
        choices=SettleStrategies.choices,
        default=SettleStrategies.SYNC_FIRST,
    )

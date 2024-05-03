from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class MoneyCurrencies(TextChoices):
    USD = "USD", _("USD")
    IRT = "IRT", _("IRT")
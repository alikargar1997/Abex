from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class SettleStrategies(TextChoices):
    SYNC_FIRST = "sync_first", _("Sync First")
    ASYNC = "async", _("Async")

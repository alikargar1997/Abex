import os
import django
from temporalio import activity
from src.exchange.temporal.dataclasses import PurchasedCryptocurrency


@activity.defn
def prepare_settlement(cryptocurrency: str) -> list[PurchasedCryptocurrency]:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    from src.exchange.const import SettlementStatuses  # noqa
    from src.exchange.models import Exchange  # noqa
    from src.abex_settings.models import AbexSettings  # noqa
    from django.db import transaction  # noqa
    from django.utils import timezone  # noqa

    abex_settings = AbexSettings.get_solo()
    purchased_cryptocurrencies = []
    with transaction.atomic():
        exchanges = Exchange.custom_objects.get_exchanges_to_settle(
            cryptocurrency
        ).select_for_update()
        if (
            sum(map(lambda x: x.total_price_amount, exchanges))
            < abex_settings.min_amount_intl_exchanges_support
        ):
            return []
        for exchange in exchanges:
            purchased_cryptocurrencies.append(
                PurchasedCryptocurrency(
                    exchange_id=exchange.id,
                    cryptocurrency=exchange.cryptocurrency.title,
                    quantity=exchange.quantity,
                )
            )
        exchanges.update(
            settlement_status=SettlementStatuses.PENDING, updated_at=timezone.now()
        )
    return purchased_cryptocurrencies

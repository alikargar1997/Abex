import os
import django
from temporalio import activity
from src.exchange.temporal.dataclasses import PurchasedCryptocurrency


@activity.defn
def settle_cryptocurrency(
    purchased_cryptocurrencies: list[PurchasedCryptocurrency],
) -> str:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    from src.exchange.models import ExchangeSettlementHistory  # noqa
    from src.exchange.const import SettlementStatuses  # noqa
    from src.exchange.utils import buy_from_exchange  # noqa

    def _create_histories(settlement_status, str, status_code: int, response: str):
        histories = []
        for purchased_cryptocurrency in purchased_cryptocurrencies:
            histories.append(
                ExchangeSettlementHistory(
                    exchange_id=purchased_cryptocurrency.exchange_id,
                    status=settlement_status,
                    status_code=status_code,
                    response=response,
                )
            )
        ExchangeSettlementHistory.objects.bulk_create(histories)

    status_code, response = buy_from_exchange(
        purchased_cryptocurrencies[0].cryptocurrency,
        sum(map(lambda x: x.quantity, purchased_cryptocurrencies)),
    )
    if not 200 <= status_code < 300:
        _create_histories(SettlementStatuses.FAILED, response, status_code, response)
        raise Exception(f"Error buying cryptocurrency: {response}")
    _create_histories(SettlementStatuses.DONE, response, status_code, response)
    return "Finished"


@activity.defn
def fulfill_exchange_settlement(
    purchased_cryptocurrencies: list[PurchasedCryptocurrency],
) -> str:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    from django.db import transaction  # noqa
    from src.exchange.models import Exchange  # noqa
    from src.exchange.const import SettlementStatuses  # noqa

    with transaction.atomic():
        Exchange.objects.select_for_update().filter(
            id__in=map(lambda x: x.exchange_id, purchased_cryptocurrencies)
        ).update(settlement_status=SettlementStatuses.DONE)
    return "Finished"

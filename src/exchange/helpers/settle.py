import asyncio
from asgiref.sync import async_to_sync
from src.abex_settings.models import AbexSettings
from src.exchange.models import Exchange
from src.core.utils.clients import TemporalClient, TemporalioClient
from src.exchange.temporal.workflows.settle import ProcessSettle
from src.exchange.temporal.workflows.settle_aggregate import ProcessSettleAggregate
from src.exchange.temporal.dataclasses import PurchasedCryptocurrency


class SettleExchangeHelper:

    def __init__(self, exchange: Exchange) -> None:
        self.exchange = exchange
        self.abex_settings = AbexSettings.get_solo()

    def settle(self):
        if (
            self.exchange.total_price_amount
            < self.abex_settings.min_amount_intl_exchanges_support
        ):
            self._settle_aggregate()
            return
        self._settle()

    @async_to_sync
    async def _settle(self):
        client: TemporalioClient = await TemporalClient().client
        purchased_cryptocurrencies = [
            PurchasedCryptocurrency(
                exchange_id=self.exchange.id,
                cryptocurrency=self.exchange.cryptocurrency.title,
                quantity=self.exchange.quantity,
            )
        ]
        await client.start_workflow(
            ProcessSettle,
            purchased_cryptocurrencies,
            id=ProcessSettle.get_workflow_id(
                self.exchange.cryptocurrency.title,
                self.exchange.created_at.timestamp() * 1000000,
            ),
            task_queue="settle-exchange-task-queue"
        )

    @async_to_sync
    async def _settle_aggregate(self):
        client: TemporalioClient = await TemporalClient().client
        await client.start_workflow(
            ProcessSettleAggregate,
            self.exchange.cryptocurrency.title,
            id=ProcessSettleAggregate.get_workflow_id(
                self.exchange.cryptocurrency.title,
                self.exchange.created_at.timestamp() * 1000000,
            ),
            task_queue="settle-exchange-task-queue"
        )

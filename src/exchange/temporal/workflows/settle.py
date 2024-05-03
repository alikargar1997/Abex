import asyncio
from temporalio import workflow
from src.exchange.temporal.dataclasses import PurchasedCryptocurrency
from src.core.utils.temporal_activities import execute_activity

with workflow.unsafe.imports_passed_through():
    from src.exchange.temporal.activities.settle_activities import (
        settle_cryptocurrency,
        fulfill_exchange_settlement,
    )


@workflow.defn
class ProcessSettle:

    @staticmethod
    def get_workflow_id(cryptocurrency: str, timestamp: int):
        return f"PROCESS-SETTLE-{cryptocurrency}-{timestamp}"

    @workflow.run
    async def run(
        self, purchased_cryptocurrencies: list[PurchasedCryptocurrency]
    ) -> str:
        await execute_activity(settle_cryptocurrency, purchased_cryptocurrencies)
        await execute_activity(fulfill_exchange_settlement, purchased_cryptocurrencies)
        return "Finished"

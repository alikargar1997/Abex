import asyncio
from temporalio import workflow
from src.exchange.temporal.dataclasses import PurchasedCryptocurrency
from src.core.utils.temporal_activities import execute_activity
from src.exchange.temporal.workflows.settle import ProcessSettle

with workflow.unsafe.imports_passed_through():
    from src.exchange.temporal.activities.settle_aggregate_activities import (
        prepare_settlement,
    )


@workflow.defn
class ProcessSettleAggregate:

    @staticmethod
    def get_workflow_id(cryptocurrency: str, timestamp: int):
        return f"PROCESS-SETTLE-AGGREGATE-{cryptocurrency}-{timestamp}"

    @workflow.run
    async def run(self, cryptocurrency: str) -> str:
        purchased_cryptocurrencies = await execute_activity(
            prepare_settlement, cryptocurrency
        )
        if purchased_cryptocurrencies:
            await workflow.execute_child_workflow(
                ProcessSettle,
                purchased_cryptocurrencies,
                id=ProcessSettle.get_workflow_id(
                    cryptocurrency, workflow.now().timestamp() * 1000000
                ),
                task_queue="settle-exchange-task-queue",
            )
        return "Finished"

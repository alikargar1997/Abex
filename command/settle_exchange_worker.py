import os
import sys
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
from concurrent.futures import ThreadPoolExecutor

async def main():
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.exchange.temporal.workflows.settle import ProcessSettle  # noqa
    from src.exchange.temporal.workflows.settle_aggregate import (
        ProcessSettleAggregate,
    )  # noqa
    from src.exchange.temporal.activities.settle_activities import (
        settle_cryptocurrency,
        fulfill_exchange_settlement,
    )  # noqa
    from src.exchange.temporal.activities.settle_aggregate_activities import (
        prepare_settlement,
    )  # noqa
    from config import settings  # noqa

    client = await Client.connect(f"{settings.TEMPORAL_HOST}:{settings.TEMPORAL_PORT}")
    worker = Worker(
        client,
        task_queue="settle-exchange-task-queue",
        workflows=[ProcessSettle, ProcessSettleAggregate],
        activities=[
            settle_cryptocurrency,
            fulfill_exchange_settlement,
            prepare_settlement,
        ],
        activity_executor=ThreadPoolExecutor(),
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

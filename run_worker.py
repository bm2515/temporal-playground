import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import BankingActivities, WalletActivities
from shared import REFUND_ORDER_TASK_QUEUE_NAME
from workflows import Refund


async def main() -> None:
    client: Client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    wallet_activities = WalletActivities()
    bank_activities = BankingActivities()
    worker: Worker = Worker(
        client,
        task_queue=REFUND_ORDER_TASK_QUEUE_NAME,
        workflows=[Refund],
        activities=[wallet_activities.withdraw, wallet_activities.deposit, bank_activities.refund],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import traceback

from temporalio.client import Client, WorkflowFailureError

from shared import REFUND_ORDER_TASK_QUEUE_NAME, OrderDetails
from workflows import Refund

async def main() -> None:
    # Create client connected to server at the given address
    client: Client = await Client.connect("localhost:7233")

    data: OrderDetails = OrderDetails(
        order_id='12345',
        user_id=1,
        amount=10
    )

    try:
        result = await client.execute_workflow(
            Refund.run,
            data,
            id="issue-cake-refund-701",
            task_queue=REFUND_ORDER_TASK_QUEUE_NAME,
        )

        print(f"Result: {result}")

    except WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())

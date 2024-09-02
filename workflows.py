from datetime import timedelta
import asyncio

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError
from activities import BankingActivities
from service import WalletService

from shared import RefundDetails, TransferDetails

with workflow.unsafe.imports_passed_through():
    from activities import WalletActivities
    from shared import OrderDetails



@workflow.defn
class Refund:
    @workflow.run
    async def run(self, order_details: OrderDetails) -> str:

        retry_policy = RetryPolicy(
            maximum_attempts=3,
            maximum_interval=timedelta(seconds=2),
            non_retryable_error_types=["InvalidWalletError", "InvalidAccountError"],
        )


        # Deposit order value to user's wallet
        deposit_output = await workflow.execute_activity_method(
            WalletActivities.deposit,
            TransferDetails(order_details.user_id, order_details.amount, 1),
            start_to_close_timeout=timedelta(seconds=5),
            retry_policy=retry_policy,
        )

        await asyncio.sleep(2)

        user_wallet = WalletService('example@wallet.com').find_wallet(1)

        workflow.logger.info(
            f"The Wallet balance for wallet ID {user_wallet.wallet_id}: {user_wallet.balance}"
        )

        if user_wallet.balance > 0:

            # Refund money to user's credit card
            try:
                withdraw_output = await workflow.execute_activity_method(
                    WalletActivities.withdraw,
                    TransferDetails(order_details.user_id, user_wallet.balance, 1),
                    start_to_close_timeout=timedelta(seconds=5),
                    retry_policy=retry_policy,
                )

                try:
                
                    refund_output = await workflow.execute_activity_method(
                        BankingActivities.refund,
                        RefundDetails("1234", user_wallet.balance, 1),
                        start_to_close_timeout=timedelta(seconds=5),
                        retry_policy=retry_policy,
                    )

                    return refund_output

                except:

                    try:

                        # refund to credit card failed, so replenish funds back to wallet
                        deposit_output = await workflow.execute_activity_method(
                            WalletActivities.deposit,
                            TransferDetails(order_details.user_id, user_wallet.balance, 1),
                            start_to_close_timeout=timedelta(seconds=5),
                            retry_policy=retry_policy,
                        )

                    except ActivityError as deposit_err:
                        workflow.logger.error(f"The deposit to the wallet has failed: {deposit_err}")
                        raise deposit_err

            except:
                workflow.logger.error(f"The refund of the order ID {order_details.order_id} has failed")
                
                








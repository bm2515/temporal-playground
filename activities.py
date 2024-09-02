import asyncio

from temporalio import activity

from service import BankingService, InvalidAccountError, WalletService, InvalidWalletError
from shared import (
    TransferDetails,
    RefundDetails
)


class WalletActivities:
    def __init__(self):
        self.wallet = WalletService('wallet-api.example.noon.com')

    @activity.defn
    async def withdraw(self, data: TransferDetails) -> str:
        reference_id = f"{data.reference_id}-withdrawal"
        try:
            confirmation = await asyncio.to_thread(
                self.wallet.withdraw, data.wallet_id, data.amount, reference_id
            )
            return confirmation
        except InvalidWalletError:
            raise
        except Exception:
            activity.logger.exception("Withdrawal failed")
            raise


    @activity.defn
    async def deposit(self, data: TransferDetails) -> str:

        reference_id = f"{data.reference_id}-deposit"
        try:
            confirmation = await asyncio.to_thread(
                self.wallet.deposit, data.wallet_id, data.amount, reference_id
            )
            return confirmation
        except InvalidWalletError:
            raise
        except Exception:
            activity.logger.exception("Deposit failed")
            raise
    

class BankingActivities:
    def __init__(self):
        self.bank = BankingService('bank-api.example.noon.com')

    @activity.defn
    async def refund(self, data: RefundDetails) -> str:
        reference_id = f"{data.reference_id}-refund"
        try:
            confirmation = await asyncio.to_thread(
                self.bank.refund_that_fails, data.account_number, data.amount, reference_id
            )
            return confirmation
        except InvalidAccountError:
            raise
        except Exception:
            activity.logger.exception("Refund failed")
            raise
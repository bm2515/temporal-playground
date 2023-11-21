# @@@SNIPSTART python-money-transfer-project-template-withdraw
import asyncio

from temporalio import activity

from banking_service import BankingService, InvalidAccountError
from shared import PaymentDetails


class BankingActivities:
    def __init__(self):
        self.bank = BankingService("bank-api.example.com")

    @activity.defn
    async def withdraw(self, data: PaymentDetails) -> str:
        reference_id = f"{data.reference_id}-withdrawal"
        try:
            confirmation = await asyncio.to_thread(
                self.bank.withdraw, data.source_account, data.amount, reference_id
            )
            return confirmation
        except InvalidAccountError:
            raise
        except Exception as error:
            activity.logger.exception("Withdrawal failed")
            raise error

    # @@@SNIPEND
    # @@@SNIPSTART python-money-transfer-project-template-deposit
    @activity.defn
    async def deposit(self, data: PaymentDetails) -> str:
        reference_id = f"{data.reference_id}-deposit"
        try:
            confirmation = await asyncio.to_thread(
                self.bank.deposit, data.target_account, data.amount, reference_id
            )
            """
            confirmation = await asyncio.to_thread(
                self.bank.deposit_that_fails,
                data.target_account,
                data.amount,
                reference_id,
            )
            """
            return confirmation
        except InvalidAccountError:
            raise
        except Exception as error:
            activity.logger.exception("Deposit failed")
            raise error

    # @@@SNIPEND

    # @@@SNIPSTART python-money-transfer-project-template-refund
    @activity.defn
    async def refund(self, data: PaymentDetails) -> str:
        reference_id = f"{data.reference_id}-refund"
        try:
            confirmation = await asyncio.to_thread(
                self.bank.deposit, data.source_account, data.amount, reference_id
            )
            return confirmation
        except InvalidAccountError:
            raise
        except Exception as error:
            activity.logger.exception("Refund failed")
            raise error

    # @@@SNIPEND

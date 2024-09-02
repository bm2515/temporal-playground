from dataclasses import dataclass

REFUND_ORDER_TASK_QUEUE_NAME = "TRANSFER_MONEY_TASK_QUEUE"


@dataclass
class PaymentDetails:
    source_account: str
    target_account: str
    amount: int
    reference_id: str


@dataclass
class OrderDetails:
    order_id: str
    user_id: int
    amount: int

@dataclass
class TransferDetails:
    wallet_id: int
    amount: int
    reference_id: int

@dataclass
class RefundDetails:
    account_number: str
    amount: int
    reference_id: int

import uuid
from dataclasses import dataclass
from typing import NoReturn


@dataclass
class InsufficientFundsError(Exception):
    """Exception for handling insufficient funds.

    Attributes:
        message: The message to display.

    Args:
        message: The message to display.

    """

    def __init__(self, message) -> None:
        self.message: str = message
        super().__init__(self.message)


@dataclass
class InvalidAccountError(Exception):
    """Exception for invalid account numbers.

    Attributes:
        message: The message to display.

    Args:
        message: The message to display.

    """

    def __init__(self, message) -> None:
        self.message: str = message
        super().__init__(self.message)

@dataclass
class InvalidWalletError(Exception):
    """Exception for invalid wallet ID.

    Attributes:
        message: The message to display.

    Args:
        message: The message to display.

    """

    def __init__(self, message) -> None:
        self.message: str = message
        super().__init__(self.message)

@dataclass
class Wallet:
    """A class representing a user's wallet

    Attributes: 
        wallet_id: The wallet ID of a user
        balance: The balance of the wallet

    Args: 
        wallet_id: The wallet ID of a user
        balance: The balance of the wallet
    """

    def __init__(self, wallet_id: int, balance: int) -> None:
        self.wallet_id: int = wallet_id
        self.balance: int = balance



@dataclass
class Account:
    """A class representing a bank account.

    Attributes:
        account_number: The account number for the account.
        balance: The balance of the account.

    Args:
        account_number: The account number for the account.
        balance: The balance of the account.
    """

    def __init__(self, account_number: str, balance: int) -> None:
        self.account_number: str = account_number
        self.balance: int = balance


@dataclass
class Bank:
    """
    A Bank with a list of accounts.

    The Bank class provides methods for finding an account with a given account number.

    Attributes:
        accounts: A list of Account objects representing the bank's accounts.
    """

    def __init__(self, accounts: list[Account]) -> None:
        self.accounts: list[Account] = accounts

    def find_account(self, account_number: str) -> Account:
        """
        Finds and returns the Account object with the given account number.

        Args:
            account_number: The account number to search for.

        Returns:
            The Account object with the given account number.

        Raises:
            ValueError: If no account with the given account number is
                found in the bank's accounts list.
        """
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        raise InvalidAccountError(f"The account number {account_number} is invalid.")

@dataclass
class WalletService:

    """
    A mock implementation of a Wallet API.

    The WalletService class provides methods for simulating deposits and withdrawals
    from user's wallets, as well as a method for simulating a deposit that always fails.

    Attributes:
        hostname: The hostname of the Wallet API service.
    """

    def __init__(self, hostname: str) -> None:
        self.hostname: str = hostname
        self.wallets: list[Wallet] = [Wallet(
            1, 10
        )]

    def withdraw(self, wallet_id: int, amount: int, reference_id: str) -> str:
        """
        Simulates a withdrawal from a user's wallet.

        Args:
            wallet_id: The wallet ID to deposit to.
            amount: The amount to deposit to the wallet.
            reference_id: An identifier for the transaction, used for idempotency.

        Returns:
            A transaction ID

        Raises:
            InvalidAccountError: If the wallet ID is invalid.
            InsufficientFundsError: If the wallet does not have enough funds
                to complete the withdrawal.
        """

        wallet = self.find_wallet(wallet_id)

        if amount > wallet.balance:
            raise InsufficientFundsError(
                f"The wallet {wallet_id} has insufficient funds to complete the withdrawl."
            )

        wallet.balance -= amount

        return self.generate_transaction_id("W")

    def deposit(self, wallet_id: int, amount: int, reference_id) -> str:
        """
        Simulates a deposit to a wallet.

        Args:
            wallet_id: The wallet_id to deposit to.
            amount: The amount to deposit to the wallet.
            reference_id: An identifier for the transaction, used for idempotency.

        Returns:
            A transaction ID.

        Raises:
            InvalidWalletError: If the wallet ID is invalid.
        """
        try:
            wallet = self.find_wallet(wallet_id)
        except InvalidWalletError:
            raise

        return self.generate_transaction_id("D")
        


    def generate_transaction_id(self, prefix: str) -> str:
        """
        Generates a transaction ID we can send back.

        Args:
            prefix: A prefix so you can identify the type of transaction.
        Returns:
            The transaction id.
        """
        return f"{prefix}-{uuid.uuid4()}"

    def find_wallet(self, wallet_id: int) -> Wallet:
        """
        Finds and returns the Wallet object with the given wallet ID.

        Args:
            wallet_id: The account number to search for.

        Returns:
            The Wallet object with the given Wallet ID.

        Raises:
            ValueError: If no wallet with the given Wallet ID is
                found.
        """
        for wallet in self.wallets:
            if wallet.wallet_id == wallet_id:
                return wallet
        raise InvalidWalletError(f"The Wallet ID {wallet_id} is invalid.")

    def get_balance(self, wallet_id: int) -> int:

        try:
            wallet = self.find_wallet(wallet_id)
            return wallet.balance
        except InvalidWalletError:
            raise








@dataclass
class BankingService:
    """
    A mock implementation of a banking API.

    The BankingService class provides methods for simulating deposits and withdrawals
    from bank accounts, as well as a method for simulating a deposit that always fails.

    Attributes:
        hostname: The hostname of the banking API service.
    """

    def __init__(self, hostname: str) -> None:
        """
        Constructs a new BankingService object with the given hostname.

        Args:
            hostname: The hostname of the banking API service.
        """
        self.hostname: str = hostname
        self.mock_bank: Bank = Bank(
            [Account("1234", 100)]
        )

    def refund(
        self, account_number: str, amount: int, reference_id: int
    ):
        
        try:
            account = self.mock_bank.find_account(account_number)
        except InvalidAccountError:
            raise

        return f'The refund to customer"s account number of amount {amount} is complete with the transaction ID {self.generate_transaction_id("D")}'

    def refund_that_fails(
        self, account_number: str, amount: int, reference_id: str
    ) -> NoReturn:
        """
        Simulates a refund to a bank account that always fails with an
        unknown error.

        Args:
            account_number: The account number to deposit to.
            amount: The amount to deposit to the account.
            reference_id: An identifier for the transaction, used for idempotency.

        Returns:
            An empty string.

        Raises:
            A ValueError exception object.
        """
        raise ValueError("This refund to the customer's bank account has failed.")

    def generate_transaction_id(self, prefix: str) -> str:
        """
        Generates a transaction ID we can send back.

        Args:
            prefix: A prefix so you can identify the type of transaction.
        Returns:
            The transaction id.
        """
        return f"{prefix}-{uuid.uuid4()}"

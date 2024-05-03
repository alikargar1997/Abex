from src.wallet.models import Wallet, WalletTransaction
from src.wallet.const import WalletActionType
from src.wallet.exceptions.api_exceptions import InsufficientBalance


class WalletHelper:
    def __init__(self, wallet: Wallet, change_amount: float, currency: str) -> None:
        self.wallet = wallet
        self.change_amount = change_amount
        self.currency = currency

    def withdraw(self) -> WalletTransaction:
        self._withdraw_wallet()
        return self._create_wallet_transition(WalletActionType.WITHDRAW)

    def deposit(self):
        self._deposit_wallet()
        return self._create_wallet_transition(WalletActionType.DEPOSIT)

    def _withdraw_wallet(self):
        if self.wallet.balance_amount < self.change_amount:
            raise InsufficientBalance()
        self.wallet.balance_amount -= self.change_amount
        self.wallet.save()

    def _deposit_wallet(self):
        self.wallet.balance_amount += self.change_amount
        self.wallet.save()

    def _create_wallet_transition(self, action: str) -> WalletTransaction:
        return WalletTransaction.objects.create(
            wallet=self.wallet,
            action=action,
            change_amount=self.change_amount,
            currency=self.currency,
        )

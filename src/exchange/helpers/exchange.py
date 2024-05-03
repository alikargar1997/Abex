from django.db import transaction
from src.cryptocurrency.models import Cryptocurrency
from src.wallet.models import Wallet, WalletTransaction
from src.wallet.helpers import WalletHelper
from src.exchange.models import Exchange
from src.exchange.const import ExchangeTypes
from src.authentication.models import User
from src.exchange.helpers.settle import SettleExchangeHelper


class ExchangeHelper:
    def __init__(
        self, cryptocurrency: Cryptocurrency, quantity: int, user: User
    ) -> None:
        self.cryptocurrency = cryptocurrency
        self.quantity = quantity
        self.user = user

    def purchase(self):
        return self._exchange(ExchangeTypes.BUY)

    def sell(self):
        return self._exchange(ExchangeTypes.SELL)

    @transaction.atomic
    def _exchange(self, exchange_type: str) -> Exchange:
        wallet: Wallet = Wallet.custom_objects.select_for_update().get(user=self.user)
        wallet_helper = WalletHelper(
            wallet,
            self.cryptocurrency.price_amount * self.quantity,
            self.cryptocurrency.currency,
        )
        wallet_transaction: WalletTransaction = (
            wallet_helper.withdraw()
            if exchange_type == ExchangeTypes.BUY
            else wallet_helper.deposit()
        )
        exchange = Exchange.objects.create(
            user=self.user,
            cryptocurrency=self.cryptocurrency,
            quantity=self.quantity,
            exchange_type=exchange_type,
            unit_price_amount=self.cryptocurrency.price_amount,
            currency=self.cryptocurrency.currency,
            wallet_transaction=wallet_transaction,
        )
        if exchange_type == ExchangeTypes.BUY:
            transaction.on_commit(SettleExchangeHelper(exchange=exchange).settle)
        return exchange

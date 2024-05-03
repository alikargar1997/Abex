import pytest
from decimal import Decimal
from src.wallet.models import Wallet, WalletTransaction
from src.core.const import MoneyCurrencies
from src.wallet.const import WalletActionType

@pytest.fixture
def wallet():
    return Wallet.objects.create(user=None, balance=Decimal('100.00'), currency=MoneyCurrencies.USD)

@pytest.fixture
def wallet_transaction(wallet):
    return WalletTransaction.objects.create(
        wallet=wallet,
        action=WalletActionType.DEPOSIT,
        change_amount=Decimal('50.00'),
        currency=MoneyCurrencies.USD
    )

@pytest.mark.django_db
def test_wallet_transaction_creation(wallet):
    transaction = WalletTransaction.objects.create(
        wallet=wallet,
        action=WalletActionType.WITHDRAWAL,
        change_amount=Decimal('20.00'),
        currency=MoneyCurrencies.USD
    )
    assert transaction.wallet == wallet
    assert transaction.action == WalletActionType.WITHDRAWAL
    assert transaction.change_amount == Decimal('20.00')
    assert transaction.currency == MoneyCurrencies.USD

@pytest.mark.django_db
def test_wallet_transaction_str_representation(wallet_transaction):
    expected_str = f"WalletTransaction(id={wallet_transaction.id}, action={wallet_transaction.action}, change_amount={wallet_transaction.change_amount}, currency={wallet_transaction.currency})"
    assert str(wallet_transaction) == expected_str

@pytest.mark.django_db
def test_wallet_transaction_related_name(wallet_transaction):
    assert wallet_transaction in wallet_transaction.wallet.transactions.all()

@pytest.mark.django_db
def test_wallet_transaction_action_choices(wallet):
    invalid_action = 'invalid_action'
    with pytest.raises(ValueError):
        WalletTransaction.objects.create(
            wallet=wallet,
            action=invalid_action,
            change_amount=Decimal('10.00'),
            currency=MoneyCurrencies.USD
        )

@pytest.mark.django_db
def test_wallet_transaction_currency_choices(wallet):
    invalid_currency = 'invalid_currency'
    with pytest.raises(ValueError):
        WalletTransaction.objects.create(
            wallet=wallet,
            action=WalletActionType.DEPOSIT,
            change_amount=Decimal('10.00'),
            currency=invalid_currency
        )

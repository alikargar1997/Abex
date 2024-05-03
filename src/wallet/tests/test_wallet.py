import pytest

from src.wallet.models import Wallet
from src.core.const import MoneyCurrencies
from src.tests.fixtures import user


@pytest.mark.django_db
def test_wallet_creation(user):
    wallet = user.wallet
    assert wallet.user == user
    assert wallet.balance_amount == 0.00
    assert wallet.currency == MoneyCurrencies.USD


@pytest.mark.django_db
def test_wallet_str_representation(user):
    wallet = user.wallet
    assert str(wallet) == wallet.user.username


@pytest.mark.django_db
def test_wallet_custom_manager(user):
    wallets = Wallet.custom_objects.filter(balance_amount__gt=0)
    user_wallet = user.wallet
    if user_wallet.balance_amount > 0:
        assert user_wallet in wallets
    else:
        assert len(wallets) == 0


@pytest.mark.django_db
def test_wallet_currency_choices():
    currency_choices = [
        choice[0] for choice in Wallet._meta.get_field("currency").choices
    ]
    assert MoneyCurrencies.USD in currency_choices
    assert MoneyCurrencies.IRT in currency_choices


@pytest.mark.django_db
def test_wallet_balance_update(user):
    wallet = user.wallet
    initial_balance = wallet.balance_amount
    wallet.balance_amount += 50.00
    wallet.save()
    updated_wallet = Wallet.objects.get(user=user)
    assert updated_wallet.balance_amount == initial_balance + 50.00

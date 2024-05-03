from django.db import models
from src.core.utils.model import BaseTimestampedModel
from src.core.const import MoneyCurrencies


class CryptocurrencyCustomManager(models.Manager):
    pass


class Cryptocurrency(BaseTimestampedModel):
    """
    Represents a cryptocurrency, including its title, description, price amount, and currency.

    Attributes:
        title (str): The title of the cryptocurrency.
        description (str): The description of the cryptocurrency.
        price_amount (Decimal): The price amount of the cryptocurrency.
        currency (str): The currency of the cryptocurrency, chosen from the MoneyCurrencies choices.
    """

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price_amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(
        max_length=5, choices=MoneyCurrencies.choices, default=MoneyCurrencies.USD
    )
    custom_objects = CryptocurrencyCustomManager()
    objects = models.Manager()

    def __str__(self) -> str:
        return self.title

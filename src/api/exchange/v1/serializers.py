from rest_framework import serializers
from src.exchange.models import Exchange
from src.cryptocurrency.models import Cryptocurrency
from src.exchange.helpers.exchange import ExchangeHelper


class CryptocurrencySerializer(serializers.ModelSerializer):
    """
    Serializer for a Cryptocurrency model.

    This serializer is used to handle the data for a Cryptocurrency model. It includes fields for the title, description, price_amount, and currency of the cryptocurrency.

    The `to_internal_value` method is overridden to filter the Cryptocurrency model by the `title` field and raise a validation error if the cryptocurrency is not found.
    """

    class Meta:
        model = Cryptocurrency
        fields = "__all__"
        read_only_fields = ("description", "price_amount", "currency")

    def to_internal_value(self, data):
        self.instance = self.Meta.model.custom_objects.filter(
            title=data["title"]
        ).first()
        if not self.instance:
            raise serializers.ValidationError("Cryptocurrency not found.")
        return self.instance


class PurchaseCryptocurrencySerializer(serializers.ModelSerializer):
    """
    Serializer for purchasing cryptocurrency on an exchange.

    This serializer is used to handle the data for purchasing cryptocurrency on an exchange. It includes fields for the cryptocurrency being purchased, the quantity, the exchange type, the unit price amount, the currency, and the total price amount.

    The `cryptocurrency` field is a nested serializer that uses the `CryptocurrencySerializer` to handle the cryptocurrency data. The `total_price_amount` field is a read-only field that is calculated based on the `quantity` and `unit_price_amount` fields.

    The `save` method is overridden to print the `kwargs` and `validated_data` before calling the parent `save` method.
    """

    cryptocurrency = CryptocurrencySerializer()
    total_price_amount = serializers.DecimalField(
        decimal_places=2, max_digits=8, read_only=True
    )

    class Meta:
        model = Exchange
        fields = (
            "cryptocurrency",
            "quantity",
            "exchange_type",
            "unit_price_amount",
            "currency",
            "total_price_amount",
        )
        read_only_fields = (
            "exchange_type",
            "unit_price_amount",
            "currency",
            "total_price_amount",
        )

    def save(self, **kwargs):
        self.validated_data.update({"user": self.context.get("request").user})
        helper = ExchangeHelper(**self.validated_data)
        return helper.purchase()

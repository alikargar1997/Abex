from dataclasses import dataclass


@dataclass
class PurchasedCryptocurrency:
    cryptocurrency: str
    quantity: int
    exchange_id: int

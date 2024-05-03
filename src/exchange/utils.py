import random
import json
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


def buy_from_exchange(cryptocurrency: str, quantity: int) -> tuple[int, str]:
    return (
        random.choices(
            [HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR],
            [10, 1, 2],
        )[0],
        json.dumps({}),
    )

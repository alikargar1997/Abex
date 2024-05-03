from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from drf_spectacular.utils import OpenApiResponse, extend_schema
from src.api.exchange.v1.serializers import PurchaseCryptocurrencySerializer


@extend_schema(
    request=PurchaseCryptocurrencySerializer,
    responses=OpenApiResponse(
        response=PurchaseCryptocurrencySerializer,
        description="A successful response with the serialized purchase data.",
    ),
)
class PurchaseCryptocurrencyApiView(GenericAPIView):
    """
    API view for purchasing cryptocurrency.

    This view handles the logic for processing a request to purchase cryptocurrency. It uses the `PurchaseCryptocurrencySerializer` to validate and save the purchase data.

    Args:
        request (rest_framework.request.Request): The incoming HTTP request.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        rest_framework.response.Response: A successful response with the serialized purchase data.
    """

    serializer_class = PurchaseCryptocurrencySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

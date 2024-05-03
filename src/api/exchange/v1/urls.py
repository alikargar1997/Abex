from django.urls import path

from src.api.exchange.v1.views import PurchaseCryptocurrencyApiView

urlpatterns = [
    path("purchase/",PurchaseCryptocurrencyApiView.as_view(),name="buy-cryptocurrency-v1")
]
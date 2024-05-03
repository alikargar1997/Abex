from django.conf import settings
from temporalio.client import Client as TemporalioClient, TLSConfig


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TemporalClient(metaclass=Singleton):
    def __init__(self):
        self._client = None

    @property
    async def client(self) -> TemporalioClient:
        if self._client is None:
            self._client = await TemporalioClient.connect(
                target_host=f"{settings.TEMPORAL_HOST}:{settings.TEMPORAL_PORT}",
                namespace=settings.TEMPORAL_NAMESPACE,
                tls=(
                    TLSConfig(
                        server_root_ca_cert=str.encode(
                            settings.TEMPORAL_CLIENT_ROOT_CA
                        ),
                        client_cert=str.encode(settings.TEMPORAL_CLIENT_CERT),
                        client_private_key=str.encode(settings.TEMPORAL_CLIENT_KEY),
                    )
                    if settings.TEMPORAL_CLIENT_ROOT_CA != ""
                    else False
                ),
            )
        return self._client

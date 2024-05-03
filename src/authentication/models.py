from django.contrib.auth.models import AbstractUser
from src.wallet.models import Wallet


class User(AbstractUser):
    """
        Extends the default Django User model to include a Wallet object for each User.

        When a new User is saved, a corresponding Wallet object is automatically created for that User.
    """

    def save(self, *args, **kwargs) -> None:
        create_wallet=False
        if not self.pk:
            create_wallet = True
        super().save(*args, **kwargs)
        if create_wallet:
            Wallet.objects.create(user=self)

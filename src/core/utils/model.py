from django.db import models


class BaseTimestampedModel(models.Model):
    """
    An abstract base model that provides created_at and updated_at timestamp fields.
    
    This model is intended to be inherited by other models that need to track when
    records were created and last updated. By making this an abstract base class,
    the timestamp fields will be automatically added to any model that inherits from
    it, without the need to define them explicitly.
    """
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

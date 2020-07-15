from django.db import models

from django.conf import settings

USER_MODEL = settings.AUTH_USER_MODEL


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Product(TimeStampModel):
    user = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL,
                             blank=True, null=True)
    title = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    price = models.PositiveSmallIntegerField(blank=False, null=True)
    amount = models.PositiveSmallIntegerField(blank=False, null=True)
    is_deleted = models.BooleanField(default=False)


class Purchase(TimeStampModel):
    user = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL,
                             blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL,
                                blank=True, null=True)
    amount = models.PositiveSmallIntegerField(blank=False, null=False)
    price = models.PositiveSmallIntegerField(blank=True, null=True)


class Refund(TimeStampModel):
    purchase = models.OneToOneField('Purchase', on_delete=models.CASCADE,
                                    blank=True, null=True)

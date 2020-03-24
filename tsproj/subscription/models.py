from datetime import datetime as dt

from django.db import models

from tsusers.models import TsUser


class TsSubscription(models.Model):
    user = models.ForeignKey(TsUser, on_delete=models.CASCADE)
    plan_id = models.CharField(max_length=100)
    start_date = models.DateField(default=dt.utcnow().today())
    valid_till = models.DateField(null=True)
    payment_id = models.CharField(max_length=37, null=True)  # uuid char length is 36

    created_at = models.DateTimeField(default=dt.utcnow())
    updated_at = models.DateTimeField(default=dt.utcnow())

    class Meta:
        ordering = ['created_at']

from datetime import datetime as dt

from django.db import models


class TsUser(models.Model):
    """usinng the user name as unique and primary key
    """
    user_name = models.CharField(max_length=100, primary_key=True, unique=True)

    created_at = models.DateTimeField(default=dt.utcnow())
    updated_at = models.DateTimeField(default=dt.utcnow())

    class Meta:
        ordering = ['created_at']

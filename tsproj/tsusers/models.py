from datetime import datetime as dt

from django.db import models


class TsUser(models.Model):
    user_name = models.CharField(db_index=True, max_length=100)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=dt.utcnow())
    updated_at = models.DateTimeField(default=dt.utcnow())

    class Meta:
        ordering = ['created_at']

from django.conf.urls import url
from . import views

app_name = "tsusers"

urlpatterns = [
    url(r'^(?P<username>^[a-zA-Z0-9]+([a-zA-Z0-9](_|-)[a-zA-Z0-9])*[a-zA-Z0-9]+$)?$',
        views.TsUserView.as_view(), name='ts_users'),
]

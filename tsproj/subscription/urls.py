from django.conf.urls import url
from . import views

app_name = "subscription"

urlpatterns = [
    url(r'^(?P<username>^[a-zA-Z0-9]+([a-zA-Z0-9](_|-)[a-zA-Z0-9])*[a-zA-Z0-9]+$)?$',
        views.TsSubscriptionView.as_view(), name='ts_subscription'),
    url(r'^(?P<username>[a-zA-Z0-9]+([a-zA-Z0-9](_|-)[a-zA-Z0-9])*[a-zA-Z0-9]+)/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})$',
        views.TsSubscriptionView.as_view(), name='ts_subscription_with_date'),
]

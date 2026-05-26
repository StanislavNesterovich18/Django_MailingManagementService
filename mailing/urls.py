from django.urls import path

from mailing import views
from mailing.apps import MailingConfig
from mailing.views import (RecipientCreateView, RecipientDeleteView, RecipientDetailView, RecipientListView,
                           RecipientUpdateView)

app_name = MailingConfig.name

urlpatterns = [
    path("", views.MailingListView.as_view(), name="mailing_list"),
    path("create_mailing/", views.MailingCreateView.as_view(), name="create_mailing"),
    path("detail_mailing/<int:pk>/", views.MailingDetailView.as_view(), name="detail_mailing"),
    path("start_mailing/<int:pk>/", views.MailingStartDetailView.as_view(), name="start_mailing"),
    path("update_mailing/<int:pk>/", views.MailingUpdateView.as_view(), name="update_mailing"),
    path("delete_mailing/<int:pk>/", views.MailingDeleteView.as_view(), name="delete_mailing"),
    path("create_recipient/", RecipientCreateView.as_view(), name="create_recipient"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipient/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("update_recipient/<int:pk>/", RecipientUpdateView.as_view(), name="update_recipient"),
    path("delete_recipient/<int:pk>/", RecipientDeleteView.as_view(), name="delete_recipient"),
]

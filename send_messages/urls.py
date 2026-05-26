from django.urls import path

from send_messages import views
from send_messages.apps import SendMessagesConfig

app_name = SendMessagesConfig.name


urlpatterns = [
    path("", views.MessageListView.as_view(), name="message_list"),
    path("create_message/", views.MessageCreateView.as_view(), name="create_message"),
    path("detail_message/<int:pk>/", views.MessageDetailView.as_view(), name="detail_message"),
    path("update_message/<int:pk>/", views.MessageUpdateView.as_view(), name="update_message"),
    path("delete_message/<int:pk>/", views.MessageDeleteView.as_view(), name="delete_message"),
]

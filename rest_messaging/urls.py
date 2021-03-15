from django.urls import re_path, path

from rest_messaging import views, models

urlpatterns = [
    path('posts/', views.MessageListAPIView.as_view(), name='get-list'),
    path('posts/create', views.create_message, name='create-message'),
    path('posts/<int:pk>', views.MessageDetailsAPIView.as_view(), name='message-details'),
    path('posts/<int:message_id>/read', views.read_message, name='read-message'),
    path('posts/download', views.MessageCsvExport.as_view(), name='messages-download'),
]

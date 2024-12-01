from django.urls import path
from .views import (
    chat_list, send_message, load_chat_history, search_users,
    get_new_messages, edit_message, delete_message, get_user_chats, get_chat_messages# Add the view here
)

urlpatterns = [
    path('', chat_list, name='chat_list'),
    path('search_users/', search_users, name='search_users'),
    path('get_new_messages/<int:chat_id>/', get_new_messages, name='get_new_messages'),

    path('send/<int:recipient_id>/', send_message, name='send_message'),

    path('load_chat_history/<int:recipient_id>/', load_chat_history, name='load_chat_history'),
    path('edit_message/<int:message_id>/', edit_message, name='edit_message'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    path('get_user_chats/', get_user_chats, name='get_user_chats'),

]

from django.urls import path
from .views import item_list, post_item,edit_item, delete_item,read_more,send_message,inbox,user_profile,business_items

urlpatterns = [
    path('', item_list, name='item_list'),
    path('post_item/', post_item, name='post_item'),
    path('edit_item/<int:pk>/', edit_item, name='edit_item'),
    path('delete_item/<int:pk>/', delete_item, name='delete_item'),
    path('read_more/<int:pk>/', read_more, name='read_more'),  # New URL pattern
    path('send_message/<int:receiver_id>/', send_message, name='send_message'),
    path('inbox/', inbox, name='inbox'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
     path('business-items/', business_items, name='business_items'),
]

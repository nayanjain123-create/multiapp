from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('signout/',views.signout,name='signout'),
    path('',views.home,name='home'),
    path('chat_app/',views.chat_app,name='chat_app'),
    path('todo_app/',views.todo_app,name='todo_app'),
    path('olx_app/',views.olx_app,name='olx_app'),
    path('add_task/',views.add_task,name='add_task'),
    path('task_add/',views.task_add,name='task_add'),
    path('task_edit/<int:id>/',views.task_edit,name='task_edit'),
    path('edit_task/<int:id>/',views.edit_task,name='edit_task'),
    path('delete_task/<int:id>/',views.delete_task,name='delete_task'),
    path("start_chat/<int:user_id>/",views.start_chat,name="start_chat"),
    path("chat/<int:room_id>/",views.chat_room,name="chat_room"),
    path("olx_app/", views.olx_app, name="olx_app"),
    path("add_product/", views.add_product, name="add_product"),
    path("mark_sold/<int:product_id>/",views.mark_sold,name="mark_sold"),
    path("my_products/",views.my_products,name="my_products"),
    path("delete_product/<int:product_id>/",views.delete_product,name="delete_product"),
    path("start_product_chat/<int:product_id>/",views.start_product_chat,name="start_product_chat"),
    path("product_chat_room/<int:room_id>/",views.product_chat_room,name="product_chat_room"),
    
]

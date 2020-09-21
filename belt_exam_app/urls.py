from django.urls import path
from . import views 

# index (/)  - Login Registration Page HTML (GET)

urlpatterns = [
    path('', views.index),
    path('wishes', views.wishes_page),
    path('wishes/edit/<int:id>', views.edit_wish_page),
    path('wishes/new', views.new_wish_page),
    path('wishes/stats', views.show_stats),
    path('logout', views.logout),
    
    # Invisible routes 
    # login - (/login) Logs the user in (POST)
    # register - (/register) Registers the user (POST)
    
    path('login', views.login),
    path('register', views.register),
    path('add_wish', views.add_wish),
    path('edit_wish/<int:id>', views.edit_wish),
    path('remove_wish/<int:id>', views.remove_wish),
    path('grant_wish/<int:id>', views.grant_wish),
    path('like_wish/<int:id>/<int:user_id>', views.like_wish)
]

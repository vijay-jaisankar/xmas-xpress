from django.urls import path

from .views import homeView,RoomListView,RoomDetailView,RoomEntryView,RoomCreateView
from .views import RoomDeleteAuthView,RoomUpdateView,RoomUpdateAuthView,makeAuthSecretSanta
from .views import createSecretSanta,sendEmailInvites,aboutView


urlpatterns = [
    path('',homeView,name='home'),
    path('about/',aboutView,name='about'),
    path('rooms/',RoomListView.as_view(),name='room_list'),
    # path('room/<int:pk>',RoomDetailView,name='room_detail'),
    path('room/<int:pk>',RoomEntryView,name='room_password'),
    path('room/new',RoomCreateView,name='room_create'),
    path('room/<int:pk>/delete',RoomDeleteAuthView,name='room_delete'),
    # path('room/<int:pk>/update',RoomUpdateView,name='room_update'),
    path('room/<int:pk>/secretSantaAuth',makeAuthSecretSanta,name='auth_secret_santa'),
    # path('room/<int:pk>/createSecretSanta',createSecretSanta,name='create_secret_santa'),
    path('room/<int:pk>/sendEmailInvites',sendEmailInvites,name='email_invites'),
]
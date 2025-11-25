"""
API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .v1 import views, squad_views

# Create router
router = DefaultRouter()
router.register(r'players', views.PlayerViewSet, basename='player')
router.register(r'rooms', views.RoomViewSet, basename='room')
router.register(r'items', views.ItemViewSet, basename='item')
router.register(r'npcs', views.NPCViewSet, basename='npc')
router.register(r'quests', views.QuestViewSet, basename='quest')
router.register(r'character', views.CharacterSheetViewSet, basename='character')

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/player/stats/', views.PlayerStatsView.as_view(), name='player-stats'),
    path('v1/world/zones/', views.ZoneListView.as_view(), name='zone-list'),

    # Squad customization endpoints
    path('v1/squad/customize/', squad_views.SquadCustomizationView.as_view(), name='squad-customize'),
    path('v1/squad/member/<int:member_id>/', squad_views.SquadMemberCustomizationView.as_view(), name='squad-member-customize'),
    path('v1/squad/swap/', squad_views.SquadMemberSwapView.as_view(), name='squad-member-swap'),
]

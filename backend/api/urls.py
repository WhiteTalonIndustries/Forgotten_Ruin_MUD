"""
API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .v1 import views, squad_views, mission_views

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
    path('v1/squad/generate/', squad_views.SquadGenerationView.as_view(), name='squad-generate'),

    # Mission endpoints
    path('v1/missions/', mission_views.MissionListView.as_view(), name='mission-list'),
    path('v1/missions/<str:mission_key>/', mission_views.MissionDetailView.as_view(), name='mission-detail'),
    path('v1/missions/<str:mission_key>/accept/', mission_views.MissionAcceptView.as_view(), name='mission-accept'),
    path('v1/missions/create-private/', mission_views.MissionCreatePrivateView.as_view(), name='mission-create-private'),

    # Player mission instance endpoints
    path('v1/player-missions/<uuid:player_mission_id>/objectives/<str:objective_key>/complete/',
         mission_views.MissionObjectiveCompleteView.as_view(), name='mission-objective-complete'),
    path('v1/player-missions/<uuid:player_mission_id>/abandon/',
         mission_views.MissionAbandonView.as_view(), name='mission-abandon'),
    path('v1/player-missions/<uuid:player_mission_id>/events/<str:event_key>/trigger/',
         mission_views.MissionEventTriggerView.as_view(), name='mission-event-trigger'),
    path('v1/player-missions/<uuid:player_mission_id>/events/<str:event_key>/choice/',
         mission_views.MissionChoiceView.as_view(), name='mission-choice'),
]

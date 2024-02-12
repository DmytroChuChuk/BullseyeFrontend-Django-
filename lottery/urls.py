from django.urls import include, path
from .views import *
from userauth.views import profile_view, CustomUserUpdateView, CustomUserDeleteView

urlpatterns = [
    path('favorites/', favorite_view, name='lottery_favorite'),
    path('recent/', recent_view, name='recent'),
    path('lottery_history/', lottery_history_view, name='lottery_history'),
    path('graphs/', graph_view, name='graph'),
    path('user_history/', user_history_view, name='user_history'),
    path('xxx/', test_view, name='testing_only'),
    path('privacy/', privacy_view, name='privacy'),
    path('terms/', terms_view, name='terms'),
    path('contact/', contact_view, name='contact'),
    path('help/', help_view, name='help'),
    path("unicorn/", include("django_unicorn.urls")),
    path("favorites/list/", FavoritesListApi.as_view()),
    path("favorites/<int:favorite_id>/delete/", FavoritesDeleteApi.as_view()),
    path('bullseye_picks/', bullseye_picks_view, name='bullseye_picks'),
    path('custom_picks/', custom_picks_view, name='custom_picks'),
    path('manual_picks/', manual_picks_view, name='manual_picks'),
    path('wheeling_picks/', wheeling_picks_view, name='wheeling_picks'),
]
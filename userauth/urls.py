from django.urls import path
from .views import profile_view, CustomUserUpdateView, CustomUserDeleteView, landing_view

urlpatterns = [
#    path('', landing_view, name='langing_view'),
    path('profile/', profile_view, name='account_profile'),
    path('<int:pk>/update/', CustomUserUpdateView.as_view(template_name='account/update.html'), name='account_update'),
    path('<int:pk>/delete/', CustomUserDeleteView.as_view(template_name='account/delete.html'), name='account_delete'),
]
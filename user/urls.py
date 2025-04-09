from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Login
    TokenRefreshView      # Refresh do token
)

urlpatterns = [
    path('criar/', views.UsuarioCreateView.as_view()),
    path('listar/', views.UsuarioListView.as_view()),
    path('atualizar/<int:id>/', views.UsuarioUpdateView.as_view()),
    path('deletar/<int:id>/', views.UsuarioDeleteView.as_view()),
    path('trocar-senha/<int:id>/', views.AtualizarSenhaView.as_view()),
    
    path('login/', views.CustomLoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

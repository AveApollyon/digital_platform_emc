from django.urls import path, reverse_lazy
from authentication import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
]

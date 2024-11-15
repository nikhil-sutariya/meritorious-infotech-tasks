from django.urls import path
from users import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('verify-user/<uidb64>/<token>/', views.verify_user, name='verify_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('admin-panel/', views.admin_panel, name='admin_panel')
]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from users import views as user_views


app_name ='users'
urlpatterns = [
	path('register/', views.register, name='register'),
	path('profile/', views.profileView, name='profile'),
	path('login/', views.loginView, name='login'),
	path('logout/', views.logoutView, name='logout'),
	path('password_reset/', 
		auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
		name='password-reset'),
	path('password_reset/done/', 
		auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
		name='password-reset-done'),
	path('password_reset_confirm/<uidb64>/<token>/', 
		auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
		name='password-reset-confirm'),
	path('password_reset_complete/', 
		auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
		name='password-reset-complete'),
]
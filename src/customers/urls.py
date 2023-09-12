from django.urls import path

from customers.views import ProfileView, ProfileUpdatePasswordView, EditProfileView

app_name = 'customers'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', EditProfileView.as_view(), name='profile_update'),
    path('profile/change-password/', ProfileUpdatePasswordView.as_view(), name='profile_password_update'),
]

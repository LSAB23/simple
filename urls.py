from .views import login, signup, change_password, reset_password, logout,reset, delete
from django.urls import path

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('change-password/', change_password, name='change_password'),
    path('reset-password/', reset_password, name='reset_password'),
    path('reset-password/<Token>/', reset, name='reset'),
    path('delete/', delete, name='delete')
]
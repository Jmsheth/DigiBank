from . import views
from django.urls import path

app_name = "login"

urlpatterns = [
    path('', views.home, name='cusHome'),
    path('login/', views.login, name='login'),
    path('auth/', views.auth, name='auth'),
    path('forgot/', views.forget, name='forgot'),
    path('reset/', views.reset, name='reset'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('resetauth/', views.resetauth, name='resetauth'),
    path('changepass/', views.changepass, name='changePass'),
    path('authreset/', views.resetpassauth, name='passauth'),
    path('logout/', views.logout, name='logout'),
    path('logout/', views.logout, name='logout'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    # URLS for Changes included by <kashif>
    path('userAccountSummary', views.userAccountSummary, name='userAccountSummary'),
]
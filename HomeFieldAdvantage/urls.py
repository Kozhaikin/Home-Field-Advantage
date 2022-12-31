from django.http import HttpResponse

# from .models import Question
from django.urls import path
from . import views

app_name = 'HomeFieldAdvantage'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('games/', views.game_page, name='games'),
    path('about_us/', views.about_us, name='about_us'),
    path('my_prediction/', views.my_prediction, name='my_prediction'),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('vector/', views.vector, name="vector"),
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

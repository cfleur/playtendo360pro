"""gamesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
import authentication.views
import myprofile.views
import games.views
import baseApp.views
import payments.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', baseApp.views.GameListHome.as_view(template_name='storeLibrary.html'), name='homePage'),
                  path('accounts/register/', authentication.views.register, name='registration'),
                  path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
                  path('accounts/profile/', myprofile.views.ProfileView.as_view(), name='profile'),
                  path('accounts/profile/edit/', myprofile.views.modify_profile, name='modify profile'),
                  path('accounts/submit/', games.views.submit_game, name='game submit'),
                  path('accounts/muhney/', myprofile.views.add_money, name='add money'),
                  path('games/<int:pk>/edit/', games.views.modify_game, name='modify game'),
                  path('logout/', authentication.views.signout, name='logout'),
                  path('games/<int:pk>/', games.views.GameDetail.as_view(template_name='game_detail.html'),
                       name='game-detail'),
                  path('play/games/<int:pk>/', login_required(games.views.PlayGame.as_view(template_name='game_play.html')),
                       name='game-play'),
                  path('pay/<int:pk>/',
                       login_required(payments.views.PayForGame.as_view(template_name='pay_for_game.html')),
                       name='pay-for-game'),
                  path('pay/error/<int:pk>', payments.views.payment_error, name='pay-error'),
                  path('pay/success/<int:pk>', payments.views.payment_success, name='pay-success'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # serving images in development

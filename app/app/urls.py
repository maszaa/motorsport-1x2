"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app.views.player import *
from app.views.series import *
from app.views.team import *
from app.views.driver import *
from app.views.season import *
from app.views.round import *
from app.views.competition import *
from app.views.documentation import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/series/', SeriesView.as_view()),
    url(r'^api/teams/', TeamView.as_view()),
    url(r'^api/drivers/', DriverView.as_view()),
    url(r'^api/seasons/', SeasonView.as_view()),
    url(r'^api/season/teams', SeasonTeamView.as_view()),
    url(r'^api/season/drivers', SeasonDriverView.as_view()),
    url(r'^api/season/competitions', SeasonCompetitionView.as_view()),
    url(r'^api/season/rounds', RoundView.as_view()),
    url(r'^api/competitions', CompetitionView.as_view()),
    url(r'^api/player/row/', PlayerRowView.as_view()),
    url(r'^api/players/', PlayerView.as_view()),

    url(r'^documentation/api', DocumentationView.as_view()),

]

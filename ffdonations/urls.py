"""fforg URL Configuration

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
from django.urls import path
from ffdonations.views import *

urlpatterns = [
    # Test stuff
    path('test', testView, name='testview'),
    # Teams
    path('teams', teams, name='teams'),
    path('teams/tracked', tracked_teams, name='teams-tracked'),
    # Participants
    path('participants', participants, name='participants'),
    path('participants/tracked', tracked_participants, name='participants-tracked'),
    # Donations
    path('donations', donations, name='donations'),
    path('donations/tracked', tracked_donations, name='donations-tracked'),
    path('donations/tracked/stats', tracked_donations_stats, name='donations-tracked-stats'),
    # Stats
    path('stats/donations/tracked', tracked_donations_stats, name='stats-donations-tracked'),
]

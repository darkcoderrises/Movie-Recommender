"""movie_recommender URL Configuration

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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login
from django.conf.urls import url
from booking_system import views as core_views
from booking_system import cviews 
from django.views.generic import RedirectView
#from movie_recommender.search import views



urlpatterns = [
    path(r'', include('booking_system.urls')),
    path(r'admin/', admin.site.urls),
    #url(r'^login/$', core_views.login, name='login'),
    #url(r'^login/$',auth_views.login, {'template_name': 'login.html'}),
    url(r'^login/$', cviews.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/default/', permanent=False)),
    url(r'^search/', include('haystack.urls')),
    url(r'^accounts/update/$', core_views.update_profile, name='update_user'),
]


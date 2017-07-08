"""because URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from education import views as core_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
  #  url(r'^accounts/profile/(?P<id>\d+)', core_views.edu_new, name='edu_new'),
    url(r'^login/education/(?P<name>.+)/$', core_views.profile, name='edu_new'),
    url(r'^company/$', core_views.company_new, name='company_new'),
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', core_views.login, name='login'),
    url(r'^authuser/$', core_views.authuser, name='authuser'),
    url(r'^profile/$', core_views.profile, name='profile'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^search/$', core_views.results, name='results'),

    # url(r'education/', include('education.urls')),
  #  url(r'^', include('LLogin.urls')),

]


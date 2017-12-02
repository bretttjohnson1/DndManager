"""DndManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from website import views as website_views

urlpatterns = [
    url(r'^$', website_views.index , name = 'index'),
    url(r'^admin/', admin.site.urls),
    url(r'^post_login/', website_views.respond_login, name= 'index'),
    url(r'^post_register/', website_views.respond_register, name= 'index'),
    url(r'^home/(?P<session_id>(.*))/$', website_views.homepage, name='home'),
    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/$', website_views.edit_character, name='edit_character'),
    url(r'^create_character/(?P<session_id>(.*))/$', website_views.create_character, name='edit_character')
]

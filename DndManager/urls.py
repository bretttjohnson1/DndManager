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

    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/delete_character/$', website_views.delete_character_entry,
        name='delete_character'),
    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/update_stats/$', website_views.save_base_stats,
        name='save_base_stats'),
    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/update_character_info/$', website_views.save_character_info,
        name='update_character_info'),

    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/add_armor/$', website_views.add_armor_entry,
        name='add_armor'),
    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/add_weapon/$', website_views.add_weapon_entry,
        name='add_weapon'),
    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/update_armor/(?P<armor_id>\d+)/$', website_views.update_armor_entry,
        name='update_armor'),
    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/update_weapon/(?P<weapon_id>\d+)/$', website_views.update_weapon_entry,
        name='update_weapon'),

    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/add_feat/$', website_views.add_feats_entry,
        name='add_feat'),
    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/update_feat/(?P<feat_id>\d+)/$', website_views.update_feats_entry,
        name='update_feat'),

    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/delete_armor/(?P<armor_id>\d+)/$', website_views.delete_armor_entry,
        name='delete_armor'),
    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/delete_weapon/(?P<weapon_id>\d+)/$', website_views.delete_weapon_entry,
        name='delete_weapon'),

    url(r'^edit_character/(?P<session_id>(.*))/(?P<character_id>\d+)/$', website_views.edit_character, name='edit_character'),
    url(r'^create_character/(?P<session_id>(.*))/$', website_views.create_character, name='create_character'),
    url(r'^create_game/(?P<session_id>(.*))/$', website_views.create_game, name='create_game'),
    url(r'^edit_game/(?P<session_id>(.*))/update/', website_views.edit_game, name='edit_game'),
    url(r'^edit_game/(?P<session_id>(.*))/$', website_views.edit_game, name='edit_game'),
]

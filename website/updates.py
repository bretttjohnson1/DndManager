from django.http import HttpResponse
from django.http import HttpResponseRedirect
from website.forms import *
from website.skills import static_skill_list
from website.views import *
from django.db import connection


def save_character_info(request, session_id, character_id):
    if session_id not in sessions:
        return fail_session(request)

    if request.method == "POST":
        form = CharacterModelForm(request.POST)
        if form.is_valid():
            name,game_id,race,classname,level = form.cleaned_data['name'],form.cleaned_data['game_id'],\
                                                      form.cleaned_data['race'],form.cleaned_data['classname'], \
                                                      form.cleaned_data['level']
            character_id = int(character_id)

            character_response = get_unique_character_instance(request, character_id)
            if type(character_response) != Character:
                return character_response
            character = character_response

            character.name=name
            character.game_id=game_id
            character.race=race
            character.classname=classname
            character.level = level
            character.save()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))


def save_base_stats(request, session_id, character_id):
    if session_id not in sessions:
        return fail_session(request)

    if request.method == "POST":
        form = BaseStatsModelForm(request.POST)
        if form.is_valid():
            stren,dex,con,inteligence,wis,cha = form.cleaned_data['str'],form.cleaned_data['dex'],form.cleaned_data['con'], \
                                      form.cleaned_data['int'],form.cleaned_data['wis'],form.cleaned_data['cha']
            character_id = int(character_id)

            stats_list = list(
                Base_Stats.objects.raw("SELECT * FROM base_stats WHERE char_id_id = %s", [str(character_id)]))

            if len(stats_list) > 1:
                return fail_invalid_db(request)

            if len(stats_list) == 0:
                return HttpResponse("NO stats of id " + str(character_id))

            base_stats = stats_list[0]
            base_stats.str=stren
            base_stats.dex=dex
            base_stats.con=con
            base_stats.int=inteligence
            base_stats.wis=wis
            base_stats.cha=cha
            base_stats.save()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))


def delete_character_entry(request, session_id, character_id):
    if session_id not in sessions:
        return fail_session(request)

    # Delete character from database, and redirect back to the edit character page
    if request.method == "GET":
        # If the weapon exists in the database, delete it. Otherwise, don't.
        cursor = connection.cursor()
        cursor.execute('DELETE FROM characters WHERE char_id = %s', [character_id])
        connection.commit()

    return HttpResponseRedirect("/home/" + session_id + "/")


def delete_game_entry(request, session_id, game_id):
    if session_id not in sessions:
        return fail_session(request)

    if request.method == "GET":
        # IF the game exists in the database, delete it. Otherwise, don't.
        cursor = connection.cursor()
        cursor.execute('DELETE FROM games WHERE game_id = %s', [game_id])
        connection.commit()

    return HttpResponseRedirect("/home/" + session_id + "/")

def update_skills_entry(request, session_id, character_id, skill_id):
    if session_id not in sessions:
        return fail_session(request)
    if request.method == "POST":
        form = SkillsModelForm(request.POST)
        if form.is_valid():
            character_id = int(character_id)
            skill_list = list(
                Skills.objects.raw("SELECT * FROM skills WHERE id = %s", [skill_id,]))

            if len(skill_list) != 1:
                return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))

            skill = skill_list[0]
            skill.ranks = form.cleaned_data["ranks"]
            skill.race_mod = form.cleaned_data["race_mod"]
            skill.class_mod = form.cleaned_data["class_mod"]

            skill.save()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))
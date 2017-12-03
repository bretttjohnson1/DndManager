from django.http import HttpResponse
from django.http import HttpResponseRedirect
from website.forms import *
from website.skills import static_skill_list
from website.views import *
from django.db import connection


def add_weapon_entry(request, session_id, character_id):
    if session_id not in sessions:
        return fail_session(request)
    if request.method == "GET":
        character_id = int(character_id)

        character_response = get_unique_character_instance(request, character_id)
        if type(character_response) != Character:
            return character_response
        character = character_response
        weapon_list = list(
            Weapon.objects.raw("SELECT * FROM weapons WHERE char_id_id = %s AND name = %s",
                               [str(character_id), ""]))

        if len(weapon_list) == 0:
            new_weapon = Weapon(char_id=character, name="",critical="x2",type="",range="",desc="")
            new_weapon.save()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))


def update_weapon_entry(request, session_id, character_id, weapon_id):
    if session_id not in sessions:
        return fail_session(request)
    if request.method == "POST":
        form = WeaponModelForm(request.POST)
        if form.is_valid():
            character_id = int(character_id)
            weapon_list = list(
                Weapon.objects.raw("SELECT * FROM weapons WHERE id = %s", [weapon_id]))

            if len(weapon_list) != 1:
                return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))

            weapon = weapon_list[0]
            weapon.name = form.cleaned_data["name"]
            weapon.number_damage_dice = form.cleaned_data["number_damage_dice"]
            weapon.type_damage_dice = form.cleaned_data["type_damage_dice"]
            weapon.damage_bonus = form.cleaned_data["damage_bonus"]
            weapon.critical = form.cleaned_data["critical"]
            weapon.type = form.cleaned_data["type"]
            weapon.range = form.cleaned_data["range"]
            weapon.quantity = form.cleaned_data["quantity"]
            weapon.desc = form.cleaned_data["desc"]
            weapon.save()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))


def delete_weapon_entry(request, session_id, character_id, weapon_id):
    if session_id not in sessions:
        return fail_session(request)

    # Delete weapon from database, and redirect back to the edit character page
    if request.method == "GET":
        # If the weapon exists in the database, delete it. Otherwise, don't.
        cursor = connection.cursor()
        cursor.execute('DELETE FROM weapons WHERE id = %s', [weapon_id])
        connection.commit()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))
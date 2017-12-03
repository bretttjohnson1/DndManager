from django.http import HttpResponse
from django.http import HttpResponseRedirect
from website.forms import *
from website.skills import static_skill_list
from website.views import *
from django.db import connection

def add_armor_entry(request, session_id, character_id):
    if session_id not in sessions:
        return fail_session(request)
    if request.method == "GET":
        character_id = int(character_id)

        armor_list = list(
            Armor.objects.raw("SELECT * FROM armors WHERE char_id_id = %s AND name = %s",
                              [str(character_id), ""]))
        if len(armor_list) > 0:
            HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))

        character_response = get_unique_character_instance(request, character_id)
        if type(character_response) != Character:
            return character_response
        character = character_response

        new_armor = Armor(char_id=character, name="",type="",desc="")
        new_armor.save()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))


def update_armor_entry(request, session_id, character_id,armor_id):
    if session_id not in sessions:
        return fail_session(request)
    if request.method == "POST":
        form = ArmorModelForm(request.POST)
        if form.is_valid():
            character_id = int(character_id)
            armor_list = list(
                Armor.objects.raw("SELECT * FROM armors WHERE id = %s", [armor_id]))

            if len(armor_list) != 1:
                return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))

            armor = armor_list[0]
            armor.name = form.cleaned_data["name"]
            armor.armor_bonus = form.cleaned_data["armor_bonus"]
            armor.armor_check_penalty = form.cleaned_data["armor_check_penalty"]
            armor.type = form.cleaned_data["type"]
            armor.desc = form.cleaned_data["desc"]

            armor.save()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))


def delete_armor_entry(request, session_id, character_id, armor_id):
    if session_id not in sessions:
        return fail_session(request)

    # Delete armor from database, and redirect back to the edit character page
    if request.method == "GET":
        # If the armor exists in the database, delete it. Otherwise, don't.
        cursor = connection.cursor()
        cursor.execute('DELETE FROM armors WHERE id = %s', [armor_id])
        connection.commit()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))
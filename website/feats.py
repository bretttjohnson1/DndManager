from django.http import HttpResponse
from django.http import HttpResponseRedirect
from website.forms import *
from website.skills import static_skill_list
from website.views import *
from django.db import connection


def add_feats_entry(request, session_id, character_id):
    if session_id not in sessions:
        return fail_session(request)
    if request.method == "GET":
        character_id = int(character_id)

        feats_list = list(
            Feats.objects.raw("SELECT * FROM feats WHERE char_id_id = %s AND name = %s",
                              [str(character_id), ""]))
        if len(feats_list) > 0:
            HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))

        character_response = get_unique_character_instance(request, character_id)
        if type(character_response) != Character:
            return character_response
        character = character_response

        new_feat = Feats(char_id=character, name="",desc="")
        new_feat.save()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))


def update_feats_entry(request, session_id, character_id,feat_id):
    if session_id not in sessions:
        return fail_session(request)
    if request.method == "POST":
        form = FeatsModelForm(request.POST)
        if form.is_valid():
            character_id = int(character_id)
            feat_list = list(
                Feats.objects.raw("SELECT * FROM feats WHERE id = %s", [feat_id]))

            if len(feat_list) != 1:
                return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))

            feat = feat_list[0]
            feat.name = form.cleaned_data["name"]
            feat.desc = form.cleaned_data["desc"]
            feat.save()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))


def delete_feat_entry(request, session_id, character_id, feat_id):
    if session_id not in sessions:
        return fail_session(request)

    if request.method == "GET":
        # IF the feat exists in the database, delete it. Otherwise, don't.
        cursor = connection.cursor()
        cursor.execute('DELETE FROM feats WHERE id = %s', [feat_id])
        connection.commit()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
import hashlib
import random
import uuid
import time
from website.models import *
from website.forms import *
from website.skills import static_skill_list

from django.db import connection
from website.skills import base_to_bonus


# Create your views here.
sessions = {}
logged_in = {}
timeout = 2700

def index(request):
    template = loader.get_template('login.html')
    context = {"loginform": LoginForm(),
               "registerform": RegisterForm(), }
    return HttpResponse(template.render(context, request))


def fail_session(request):
        template = loader.get_template('login.html')
        context = {"loginform": LoginForm(),
                   "registerform": RegisterForm(),
                   "login_err_mesg": "Error: invalid session id"}

        return HttpResponse(template.render(context, request))

def fail_invalid_db(request):
    return HttpResponse("Error: database corrupted")

def get_unique_character_instance(request, character_id):
    characters = list(
        Character.objects.raw("SELECT * FROM characters WHERE char_id = %s", [str(character_id), ]))

    if len(characters) > 1:
        return fail_invalid_db(request)

    if len(characters) == 0:
        return HttpResponse("NO stats of id " + str(character_id))

    return characters[0]


def login_user(username):

    if username in logged_in:
        if logged_in[username][1] < 2700:
            return HttpResponseRedirect("/home/" + logged_in[username][0] + "/")
        else:
            del logged_in[username]

    session_key = str(uuid.uuid4())
    logged_in[username] = (session_key,(time.time() * 1000000))
    sessions[session_key] = username

    return HttpResponseRedirect("/home/" + session_key + "/")


def respond_login(request):
    def fail_login(request):
        template = loader.get_template('login.html')
        context = {"loginform": LoginForm(),
                   "registerform": RegisterForm(),
                   "login_err_mesg": "Error: incorrect username or password"}

        return HttpResponse(template.render(context, request))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = str(form.cleaned_data['password'])

            # num_results = User.objects.filter(account_name=username).count()

            # gets the first and only value
            results = list(User.objects.raw("SELECT * from users where account_name = %s", [username]))

            if len(results) == 0:
                return fail_login(request)

            result = results[0]
            salt = result.password_salt

            combined = str.encode(salt + password)
            passhash = hashlib.sha256(combined).hexdigest()

            if passhash == result.password_hash:
                return login_user(username)

            return fail_login(request)
            # return HttpResponseRedirect("/home/")

    return HttpResponse("Failed: This link is for post requests")


def respond_register(request):
    def register_fail(request, message):
        template = loader.get_template('login.html')
        context = {"loginform": LoginForm(),
                   "registerform": RegisterForm(),
                   "register_err_mesg": "Error: " + message + " "}

        return HttpResponse(template.render(context, request))

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            salt = ''.join(list(map(chr, [random.randint(97, 122) for i in range(7)])))

            password = str(form.cleaned_data['password'])
            if password != str(form.cleaned_data['confirm_password']):
                return register_fail(request, "passwords must match")

            combined = str.encode(salt + password)
            passhash = hashlib.sha256(combined).hexdigest()

            # num_results = User.objects.filter(account_name=username).count()

            num_results = len(list(User.objects.raw("SELECT * from users where account_name = %s", [username])))
            if num_results > 0:
                return register_fail(request, "User already exists")

            new_user = User(account_name=form.cleaned_data['username'], password_hash=passhash, password_salt=salt)
            new_user.save()

            return login_user(username)
            # return HttpResponseRedirect("/home/")

    return HttpResponse("Error: This link is for post requests")


def homepage(request, session_id):
    if request.method == "POST":
        return HttpResponse("Error: Homepage link is for get requests")

    if session_id not in sessions:
        return fail_session(request)
    user = User.objects.filter(account_name=sessions[session_id])
    games_list = Game.objects.filter(ran_by=user)

    gameformlist = []

    for game in games_list:
        chars_in_game = Character.objects.filter(game_id=game)
        charlist = []
        for chars in chars_in_game:
            charlist.append(str(chars.name))

        gameformlist.append((game.game_id, str(game.game_name), charlist))


    template = loader.get_template('homepage.html')
    characters = Character.objects.raw("SELECT * FROM characters WHERE user_name_id = %s",[sessions[session_id]])
    context = {"characters": characters,
               "username": sessions[session_id],
               "session_id": session_id,
               "gameforms": gameformlist}
    return HttpResponse(template.render(context, request))

def create_game(request, session_id):
    def fail_login(request):
        template = loader.get_template('login.html')
        context = {"loginform": LoginForm(),
                   "registerform": RegisterForm(),
                   "login_err_mesg": "Incorrect session_id, it does not exist in the dictionary"}

        return HttpResponse(template.render(context, request))

    # Check if a session id is a valid id
    if session_id not in sessions:
        return fail_login(request)
    if request.method == "GET":
        return HttpResponseRedirect("/edit_game/" + session_id + "/")

    return HttpResponse("Failed: create_game is for get requests")

def edit_game(request, session_id):
    def fail_login(request):
        template = loader.get_template('login.html')
        context = {"loginform": LoginForm(),
                   "registerform": RegisterForm(),
                   "login_err_mesg": "Incorrect session_id, it does not exist in the dictionary"}

        return HttpResponse(template.render(context, request))

    # Check if a session id is a valid id
    if session_id not in sessions:
        return fail_login(request)
    if request.method == "GET":
        template = loader.get_template('edit_game.html')
        context = {"gameform": GameModelForm(),}

        return HttpResponse(template.render(context, request))

    if request.method == "POST":
        form = GameModelForm(request.POST)
        if form.is_valid():
            # Read game data
            name = form.cleaned_data['game_name']
            dm = list(User.objects.raw("SELECT * FROM users WHERE account_name = %s", [sessions[session_id]]))[0]

            # Create game
            g = Game(game_name=name, ran_by=dm)
            g.save()
            return HttpResponseRedirect("/home/" + session_id + "/")

    return HttpResponseRedirect("/home/" + session_id + "/")


# This is called from the create_character/session_id
def create_character(request, session_id):
    def fail_login(request):
        template = loader.get_template('login.html')
        context = {"loginform": LoginForm(),
                   "registerform": RegisterForm(),
                   "login_err_mesg": "Incorrect session_id, it does not exist in the dictionary"}

        return HttpResponse(template.render(context, request))

    # Check if a session id is even valid id
    if session_id not in sessions:
        return fail_login(request)

    if request.method == "GET":
        # Since user_name is a non-null foreign key, get the character's name from the map
        foreignUsers = User.objects.raw("SELECT * FROM users WHERE account_name = %s", [sessions[session_id]])
        foreignuser = foreignUsers[0] # Because we want the user, and not the user as part of a list

        # insert a character, the auto incrementing field sets the char_id already
        c = Character(name='default_name', user_name=foreignuser, game_id=None, classname='', level=0)
        c.save()

        # Also set base stats to the database
        b = Base_Stats(char_id=c)
        b.save()

        static_skills = static_skill_list()
        for skill in static_skills:
            skillmodel = Skills(char_id=c, skill_name=skill[0],relevant_ability=skill[1])
            skillmodel.save()

        # Now we pass this into edit_character
        created_char_id = c.char_id

        # Print out a httpResponse to test
        return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(created_char_id))

    return HttpResponse("Failed: Create Character link is for get requests")


def edit_character(request, session_id, character_id):
    if request.method == "POST":
        return HttpResponse("Error: Edit Character link is for get requests")

    if session_id not in sessions:
        return fail_session(request)

    username = sessions[session_id]

    character_response = get_unique_character_instance(request, character_id)
    if type(character_response) != Character:
        return character_response
    character = character_response


    stats_list = list(Base_Stats.objects.raw("SELECT * FROM base_stats WHERE char_id_id = %s",[str(character_id),]))
    weapons_list = list(Weapon.objects.raw("SELECT * FROM weapons WHERE char_id_id = %s", [str(character_id), ]))
    armor_list = list(Armor.objects.raw("SELECT * FROM armors WHERE char_id_id = %s", [str(character_id), ]))
    feats_list = list(Feats.objects.raw("SELECT * FROM feats WHERE char_id_id = %s", [str(character_id), ]))
    skills_list = list(Skills.objects.raw("SELECT * FROM skills WHERE char_id_id = %s", [str(character_id), ]))

    character_race = \
    list(Static_Race.objects.raw("SELECT * FROM static_race WHERE race_name = %s", [str(character.race_id), ]))[0]

    if len(stats_list) > 1:
        return fail_invalid_db(request)
    if len(stats_list) == 0:
        return HttpResponse("NO stats of id " + str(character_id))

    stats = stats_list[0]
    stats_names = ["str", "con", "dex", "int", "wis", "cha"]

    stat_values = [(stats.str + character_race.strmod),
                    (stats.con + character_race.conmod),
                    (stats.dex + character_race.dexmod),
                    (stats.int + character_race.intmod),
                    (stats.wis + character_race.wismod),
                    (stats.cha + character_race.chamod)]
    stat_bonuses = list(map(base_to_bonus, stat_values))

    stat_map = {k:v for k,v in zip(stats_names,stat_bonuses)}

    character_form = CharacterModelForm(instance=character)
    character_form_data = FormData("Character Info","update_character_info",None,"delete_character")
    stats_form =  BaseStatsModelForm(instance=stats)
    stats_form_data = FormData("Character Stats","update_stats")
    weapons_list_forms = []
    armor_list_forms = []
    feats_list_forms = []

    skills_list_forms = []
    for weapon in weapons_list:
        weapons_list_forms.append((int(weapon.id), WeaponModelForm(instance=weapon)))

    for armor in armor_list:
        armor_list_forms.append((int(armor.id), ArmorModelForm(instance=armor)))

    for feats in feats_list:
        feats_list_forms.append((int(feats.id), FeatsModelForm(instance=feats)))

    for skills in skills_list:
        # todo calculate total skill mod
        skillform = SkillsModelForm(instance=skills)
        stat = stat_map[str(skills.relevant_ability).lower()]
        if int(skills.class_mod) >= 1:
            stat += 3 + int(skills.class_mod) - 1
        stat += int(skills.race_mod)
        if int(skills.ranks) > 0:
            stat += skills.ranks
        else:
            stat = 0

        skills_list_forms.append((int(skills.id), skillform,
                                 SkillData(str(skills.skill_name), str(skills.relevant_ability), stat)))


    weapon_form_data = FormData("Weapons","update_weapon", "add_weapon", "delete_weapon")
    armor_form_data = FormData("Armor", "update_armor", "add_armor", "delete_armor")
    feats_form_data = FormData("Feats", "update_feat", "add_feat","delete_feat")
    skills_form_data = FormData("Skills", "update_skill")

    formlist = [character_form, stats_form]
    formdatalist = [character_form_data, stats_form_data]

    multiformlist = [weapons_list_forms,armor_list_forms,feats_list_forms]
    multiformdatalist = [weapon_form_data, armor_form_data, feats_form_data]

    template = loader.get_template('edit_character.html')
    context = {}
    context["forms"] = zip(formlist, formdatalist)
    context["multiforms"] = zip(multiformlist,multiformdatalist)
    context["skillmultiforms"] =  skills_list_forms
    context["skillformdata"] = skills_form_data
    context["username"] = username

    # display stats

    context["stats"] = zip(stats_names, stat_bonuses)

    return HttpResponse(template.render(context, request))

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from website.forms import LoginForm
from website.forms import RegisterForm
import hashlib
import random
import uuid
import time
from website.models import *
from website.forms import *


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
                return register_fail(request,"User already exists")

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

    template = loader.get_template('homepage.html')
    for i in sessions:
        print(i, sessions[i])
    characters = Character.objects.raw("SELECT * FROM characters WHERE user_name_id = %s",[sessions[session_id]])
    context = {"characters": characters,
               "username": sessions[session_id],
               "session_id": session_id}
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
        print("RECieved post")
        form = GameModelForm(request.POST)
        if form.is_valid():
            # Read game data
            name = form.cleaned_data['game_name']
            dm = form.cleaned_data['ran_by']

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

    if len(stats_list) > 1:
        return fail_invalid_db(request)
    if len(stats_list) == 0:
        return HttpResponse("NO stats of id " + str(character_id))

    stats = stats_list[0]
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
        skills_list_forms.append((int(skills.id), FeatsModelForm(instance=skills)))


    weapon_form_data = FormData("Weapons","update_weapon", "add_weapon", "delete_weapon")
    armor_form_data = FormData("Armor", "update_armor", "add_armor", "delete_armor")
    feats_form_data = FormData("Feats", "update_feat", "add_feat","delete_feat")
    skills_form_data = FormData("Skills", "update_skill")

    formlist = [character_form, stats_form]
    formdatalist = [character_form_data, stats_form_data]

    multiformlist = [weapons_list_forms,armor_list_forms,feats_list_forms, skills_list_forms]
    multiformdatalist = [weapon_form_data, armor_form_data, feats_form_data, skills_form_data]

    template = loader.get_template('edit_character.html')
    context = {"forms": zip(formlist, formdatalist),
               "multiforms": zip(multiformlist,multiformdatalist),
               "username": username}

    return HttpResponse(template.render(context, request))

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


def update_skills_entry(request, session_id, character_id, skill_id):
    if session_id not in sessions:
        return fail_session(request)
    if request.method == "POST":
        form = SkillsModelForm(request.POST)
        if form.is_valid():
            character_id = int(character_id)
            feat_list = list(
                Skills.objects.raw("SELECT * FROM feats WHERE id = %s", [skill_id]))

            if len(feat_list) != 1:
                return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))

            feat = feat_list[0]
            feat.name = form.cleaned_data["ranks"]
            feat.save()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))

def delete_armor_entry(request, session_id, character_id, armor_id):
    if session_id not in sessions:
        return fail_session(request)

    # Delete armor from database, and redirect back to the edit character page
    if request.method == "GET":
        # If the armor exists in the database, delete it. Otherwise, don't.
        armors = Armor.objects.raw("SELECT * FROM armors WHERE id = %s", [armor_id])

        for armor in armors:
            armor.delete()
    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))


def delete_weapon_entry(request, session_id, character_id, weapon_id):
    if session_id not in sessions:
        return fail_session(request)

    # Delete weapon from database, and redirect back to the edit character page
    if request.method == "GET":
        # If the weapon exists in the database, delete it. Otherwise, don't.
        weapons = Weapon.objects.raw("SELECT * FROM weapons WHERE id = %s", [weapon_id])

        for weapon in weapons:
            weapon.delete()

    return HttpResponseRedirect("/edit_character/" + session_id + "/" + str(character_id))

def delete_character_entry(request, session_id, character_id):
    if session_id not in sessions:
        return fail_session(request)

    # Delete weapon from database, and redirect back to the edit character page
    if request.method == "GET":
        # If the weapon exists in the database, delete it. Otherwise, don't.
        characters = Character.objects.raw("SELECT * FROM characters WHERE char_id = %s", [character_id])

        for character in characters:
            character.delete()

    return HttpResponseRedirect("/home/" + session_id + "/")
from django.db import models

# Create your models here.

class Static_Race(models.Model):
    race_name = models.CharField(max_length=40, primary_key=True)
    strmod = models.IntegerField
    dexmod = models.IntegerField
    conmod = models.IntegerField
    intmod = models.IntegerField
    wismod = models.IntegerField
    chamod = models.IntegerField


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=40)
    password_hash = models.CharField(max_length=40)

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=40)
    ran_by = models.ForeignKey(User, on_delete=models.CASCADE)



class Character(models.Model):
    char_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    race = models.ForeignKey(Static_Race)
    classname = models.CharField(max_length=40)
    level = models.IntegerField


class Inventory(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=40)
    item_desc = models.CharField(max_length=40)
    quantity = models.IntegerField

    class Meta:
        unique_together = (("char_id", "item_name"))


class Weapon(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    number_damage_dice = models.IntegerField
    type_damage_dice = models.IntegerField
    damage_bonus = models.IntegerField
    critical = models.CharField(max_length=40)
    type = models.CharField(max_length=40)
    range = models.CharField(max_length=40)
    quantity = models.IntegerField
    desc = models.CharField(max_length=4000)
    class Meta:
        unique_together = (("char_id", "name"))


class Armor(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    armor_bonus = models.IntegerField
    armor_check_penalty = models.IntegerField
    type = models.CharField(max_length=40)
    desc = models.CharField(max_length=4000)
    class Meta:
        unique_together = (("char_id", "name"))


class Base_Stats(models.Model):
    char_id = models.ForeignKey(Character, primary_key=True, on_delete=models.CASCADE)
    str = models.IntegerField
    dex = models.IntegerField
    con = models.IntegerField
    int = models.IntegerField
    wis = models.IntegerField
    cha = models.IntegerField


class Feats(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    desc = models.CharField(max_length=400)
    class Meta:
        unique_together = (("char_id", "name"))


class Skills(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=40)
    abilit_choices = [
        ("str","str"),
        ("dex","dex"),
        ("con","con"),
        ("int","int"),
        ("wis","wis"),
        ("cha","cha")

    ]
    relevant_ability = models.CharField(max_length=3, choices=abilit_choices)
    ranks = models.IntegerField
    class_mod = models.IntegerField
    race_mod = models.IntegerField
    class Meta:
        unique_together = (("char_id", "skill_name"))


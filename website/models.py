from django.db import models

# Create your models here.

class Static_Race(models.Model):
    race_name = models.CharField(max_length=40, primary_key=True)
    strmod = models.IntegerField(default=0)
    dexmod = models.IntegerField(default=0)
    conmod = models.IntegerField(default=0)
    intmod = models.IntegerField(default=0)
    wismod = models.IntegerField(default=0)
    chamod = models.IntegerField(default=0)
    class Meta:
        db_table = "static_race"
    def __str__(self):
        return self.race_name


class User(models.Model):
    account_name = models.CharField(primary_key=True, max_length=40)
    password_salt = models.CharField(default="",max_length=40)
    password_hash = models.CharField(max_length=512)
    class Meta:
        db_table = "users"
    def __str__(self):
        return self.account_name

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=40)
    ran_by = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = "games"
    def __str__(self):
        return self.game_name

class Character(models.Model):
    char_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    race = models.ForeignKey(Static_Race, default="Half-Orc")
    classname = models.CharField(max_length=40)
    level = models.IntegerField(default=0)
    class Meta:
        db_table = "characters"
    def __str__(self):
        return self.name


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=40)
    item_desc = models.CharField(max_length=40)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = (("char_id", "item_name"),)
        db_table = "inventories"
    def __str__(self):
        return self.item_name


class Weapon(models.Model):
    id = models.AutoField(primary_key=True)
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    number_damage_dice = models.IntegerField(default=0)
    type_damage_dice = models.IntegerField(default=0)
    damage_bonus = models.IntegerField(default=0)
    critical = models.CharField(max_length=40)
    type = models.CharField(max_length=40)
    range = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    desc = models.CharField(max_length=4000)
    class Meta:
        unique_together = (("char_id", "name"),)
        db_table = "weapons"
    def __str__(self):
        return str(self.id)


class Armor(models.Model):
    id = models.AutoField(primary_key=True)
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    armor_bonus = models.IntegerField(default=0)
    armor_check_penalty = models.IntegerField(default=0)
    type = models.CharField(max_length=40)
    desc = models.CharField(max_length=4000)
    quantity = models.IntegerField(default=1)
    class Meta:
        unique_together = (("char_id", "name"),)
        db_table = "armors"
    def __str__(self):
        return str(self.id)


class Base_Stats(models.Model):
    char_id = models.ForeignKey(Character, primary_key=True, on_delete=models.CASCADE)
    str = models.IntegerField(default=0)
    dex = models.IntegerField(default=0)
    con = models.IntegerField(default=0)
    int = models.IntegerField(default=0)
    wis = models.IntegerField(default=0)
    cha = models.IntegerField(default=0)
    class Meta:
        db_table = "base_stats"
    def __str__(self):
        return str(self.char_id)


class Feats(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    desc = models.CharField(max_length=400)
    class Meta:
        unique_together = (("char_id", "name"),)
        db_table = "feats"
    def __str__(self):
        return self.name


class Skills(models.Model):
    char_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=40)
    ability_choices = [
        ("str","str"),
        ("dex","dex"),
        ("con","con"),
        ("int","int"),
        ("wis","wis"),
        ("cha","cha")

    ]
    relevant_ability = models.CharField(max_length=3, choices=ability_choices)
    ranks = models.IntegerField(default=0)
    class_mod = models.IntegerField(default=0)
    race_mod = models.IntegerField(default=0)
    class Meta:
        unique_together = (("char_id", "skill_name"),)
        db_table = "skills"
    def __str__(self):
        return self.name


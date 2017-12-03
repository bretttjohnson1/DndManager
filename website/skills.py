def static_skill_list():
    static_skills = ['Acrobatics', 'Appraise', 'Bluff', 'Climb', 'Craft', 'Diplomacy', 'Disable Device', 'Disguise',
                     'Escape Artist', 'Fly', 'Handle Animal', 'Heal', 'Intimidate', 'Knowledge (arcana)',
                     'Knowledge(dungeoneering)', 'Knowledge(engineering)', 'Knowledge(geography)',
                     'Knowledge (history)',
                     'Knowledge (local)', 'Knowledge (nature)', 'Knowledge (nobility)', 'Knowledge (planes)',
                     'Knowledge (religion)', 'Linguistics', 'Perception', 'Perform', 'Profession', 'Ride',
                     'Sense Motive',
                     'Sleight of Hand', 'Spellcraft', 'Stealth', 'Survival', 'Swim', 'Use Magic Device']
    skill_stats = ['Dex', 'Int', 'Cha', 'Str', 'Int', 'Cha', 'Dex', 'Cha', 'Dex', 'Dex', 'Cha', 'Wis', 'Cha', 'Int',
                   'Int', 'Int',
                   'Int', 'Int', 'Int', 'Int', 'Int', 'Int', 'Int', 'Int', 'Wis', 'Cha', 'Wis', 'Dex', 'Wis', 'Dex',
                   'Int', 'Dex',
                   'Wis', 'Str']

    return list(zip(static_skills,skill_stats))

import json
import theo_utils
import random
from question_types import QuestionType


def get_and_save_all_heroes():
    source_file = open(theo_utils.get_dota_folder_path() + 'npc_heroes.txt',
                       'r')
    valve_string = source_file.read()
    json_string = theo_utils.valve_string_to_json_string(valve_string)

    heroes_valve = json.loads(json_string)['DOTAHeroes']
    json_string = json.dumps(heroes_valve, indent=4)
    destination_file = open('heroes_valve_format.json', 'w+')
    destination_file.write(json_string)
    destination_file.close()

    heroes_custom = valve_format_to_custom_format(heroes_valve)
    json_string = json.dumps(heroes_custom, indent=4)
    destination_file = open('heroes_custom_format.json', 'w+')
    destination_file.write(json_string)
    destination_file.close()

    return heroes_custom


def valve_format_to_custom_format(heroes_valve):
    heroes_custom = dict()
    name_filter = ["Version", "npc_dota_hero_base", "npc_dota_hero_target_dummy"]
    kept_attributes = ["ArmorPhysical", "MagicalResistance", "AttackCapabilities", "AttackDamageMin", "AttackDamageMax",
                       "AttackRate", "AttackRange", "ProjectileSpeed", "AttributePrimary", "AttributeBaseStrength",
                       "AttributeStrengthGain", "AttributeBaseIntelligence", "AttributeIntelligenceGain",
                       "AttributeBaseAgility", "AttributeAgilityGain", "RingRadius", "MovementSpeed",
                       "MovementTurnRate", "StatusHealthRegen", "StatusHealth", "StatusMana", "StatusManaRegen",
                       "VisionDaytimeRange", "VisionNighttimeRange"]
    base_values = dict()
    base_values["StatusHealthRegen"] = 0
    for hero_name in heroes_valve:
        try:
            if hero_name in name_filter:
                continue
            hero_valve = heroes_valve[hero_name]
            hero_custom = dict()
            hero_custom["name"] = hero_name
            for attribute in kept_attributes:
                if attribute in hero_valve.keys():
                    hero_custom[attribute] = hero_valve[attribute]
                elif attribute in heroes_valve["npc_dota_hero_base"].keys():
                    hero_custom[attribute] = heroes_valve["npc_dota_hero_base"][attribute]
                else:
                    hero_custom[attribute] = base_values[attribute]
                try:
                    hero_custom[attribute] = float(hero_custom[attribute])
                    if hero_custom[attribute].is_integer():
                        hero_custom[attribute] = int(hero_custom[attribute])
                except ValueError:
                    pass
                hero_custom[attribute] = [hero_custom[attribute]]

            add_custom_attributes(hero_custom)

            heroes_custom[hero_name] = hero_custom
        except Exception as error:
            print("ERROR BY " + hero_name + "\n\t" + str(error))

    return heroes_custom


def add_custom_attributes(hero):
    constants = theo_utils.get_dota_constants()
    hero["Custom_HpLvl1"] = [hero["StatusHealth"][0] + hero["AttributeBaseStrength"][0] * constants["hp_per_str"]]
    hero["Custom_ManaLvl1"] = [
        hero["StatusMana"][0] + hero["AttributeBaseIntelligence"][0] * constants["mana_per_int"]]
    hero["Custom_ArmorLvl1"] = [
        hero["ArmorPhysical"][0] + hero["AttributeBaseAgility"][0] * constants["armor_per_agi"]]
    hero["Custom_HpRegenLvl1"] = [
        hero["StatusHealthRegen"][0] + hero["AttributeBaseStrength"][0] * constants["hp_regen_per_str"]]
    hero["Custom_ManaRegenLvl1"] = [
        hero["StatusManaRegen"][0] + hero["AttributeBaseIntelligence"][0] * constants["mana_regen_per_int"]]
    hero["Custom_MagicResistanceLvl1"] = [1 - (1 - hero["MagicalResistance"][0] / 100) * (
                1 - hero["AttributeBaseStrength"][0] * constants["magic_res_per_str"])]
    dmg = round((hero["AttackDamageMin"][0] + hero["AttackDamageMax"][0]) / 2)
    primary_attribute = hero["AttributePrimary"][0]
    if primary_attribute == "DOTA_ATTRIBUTE_STRENGTH":
        bonus = hero["AttributeBaseStrength"]
    elif primary_attribute == "DOTA_ATTRIBUTE_AGILITY":
        bonus = hero["AttributeBaseAgility"]
    elif primary_attribute == "DOTA_ATTRIBUTE_INTELLECT":
        bonus = hero["AttributeBaseIntelligence"]
    hero["Custom_AttackDamageLvl1"] = [dmg + bonus[0]]


def get_corresponding_attribute(question_type):
    possible_stats = ["Strength", "Agility", "Intelligence"]

    if question_type == QuestionType.HERO_STARTING_STATS:
        stat = random.choice(possible_stats)
        return "AttributeBase" + stat
    elif question_type == QuestionType.HERO_STAT_GAIN:
        stat = random.choice(possible_stats)
        return "Attribute" + stat + "Gain"
    elif question_type == QuestionType.HERO_TURN_RATE:
        return "MovementTurnRate"
    elif question_type == QuestionType.HERO_ATTACK_RANGE:
        return "AttackRange"
    elif question_type == QuestionType.HERO_VISION_RANGE:
        possible_time = ["Day", "Night"]
        return "Vision" + random.choice(possible_time) + "timeRange"
    elif question_type == QuestionType.HERO_PROJECTILE_SPEED:
        return "ProjectileSpeed"
    elif question_type == QuestionType.HERO_HP_LVL1:
        return "Custom_HpLvl1"
    elif question_type == QuestionType.HERO_MANA_LVL1:
        return "Custom_ManaLvl1"
    elif question_type == QuestionType.HERO_ARMOR_LVL1:
        return "Custom_ArmorLvl1"
    elif question_type == QuestionType.HERO_HP_REGEN_LVL1:
        return "Custom_HpRegenLvl1"
    elif question_type == QuestionType.HERO_MANA_REGEN_LVL1:
        return "Custom_ManaRegenLvl1"
    elif question_type == QuestionType.HERO_MAGIC_RES_LVL1:
        return "Custom_MagicResistanceLvl1"
    elif question_type == QuestionType.HERO_ATTACK_DAMAGE_LVL1:
        return "Custom_AttackDamageLvl1"

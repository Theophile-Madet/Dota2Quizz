import vpk
import theo_utils
import json
import random
import os.path
import file_paths
from question_types import QuestionType


def get_and_save_all_items():
    create_items_custom_file_if_necessary()
    return theo_utils.load_json_in_file(file_paths.items_custom_format())


def create_items_custom_file_if_necessary():
    if not os.path.isfile(file_paths.items_custom_format()):
        create_items_custom_file()
        return

    valve_file_path = file_paths.vpk_source_file()
    valve_file_modification_date = os.path.getmtime(valve_file_path)
    custom_file_modification_date = os.path.getmtime(file_paths.items_custom_format())
    if valve_file_modification_date > custom_file_modification_date:
        create_items_custom_file()


def create_items_custom_file():
    pak = vpk.open(file_paths.vpk_source_file())
    items_file = pak.get_file(file_paths.items_source_file_inside_vpk())

    valve_string = items_file.read().decode('utf-8')
    json_string = theo_utils.valve_string_to_json_string(valve_string)

    items_valve = json.loads(json_string)['DOTAAbilities']
    json_string = json.dumps(items_valve, indent=4)
    destination_file = open(file_paths.items_valve_format(), 'w+')
    destination_file.write(json_string)
    destination_file.close()

    items_custom = valve_format_to_custom_format(items_valve)
    json_string = json.dumps(items_custom, indent=4)
    destination_file = open(file_paths.items_custom_format(), 'w+')
    destination_file.write(json_string)
    destination_file.close()


def valve_format_to_custom_format(items_valve):
    items_custom = dict()
    name_filter = ["Version", "item_super_blink", "item_pocket_tower", "item_pocket_roshan", "item_mutation_tombstone"]
    attribute_filter = ["EventID", "IsObsolete"]
    kept_attributes = ['AbilityCastRange', 'AbilityCastPoint', 'AbilityCooldown', 'AbilityManaCost', 'ItemCost',
                       'SideShop', 'SecretShop', 'ItemInitialCharges', 'IsTempestDoubleClonable',
                       'ItemStockTime', 'ItemStockInitial', 'ItemStockMax', 'ItemInitialStockTime', 'ItemRecipe',
                       'ItemResult', 'ItemRequirements', 'ItemDisassembleRule', 'AbilityChannelTime',
                       'AbilityUnitDamageType', 'SpellImmunityType', 'AbilityName']
    convert_to_number_attribute = ["ItemCost", "AbilityCastRange", "AbilityCastPoint", "AbilityCooldown",
                                   "AbilityManaCost"]

    for item_name in items_valve:
        item_valve = items_valve[item_name]
        if item_name in name_filter:
            continue
        skip = False
        for attribute in attribute_filter:
            if attribute in item_valve:
                skip = True
                break

        if skip:
            continue

        item_custom = dict()
        item_custom["name"] = item_name

        special_conversions = get_special_conversions()

        if "AbilitySpecial" in item_valve:
            for special_index in item_valve["AbilitySpecial"]:
                special = item_valve["AbilitySpecial"][special_index]
                for key in special.keys():
                    if key in special_conversions:
                        item_valve[special_conversions[key]] = special[key]

        for attribute in item_valve:
            if attribute in kept_attributes or attribute.startswith("Passive"):
                item_custom[attribute] = [item_valve[attribute]]
                if attribute in convert_to_number_attribute or attribute.startswith("Passive"):
                    attribute_string_value = item_valve[attribute]
                    values = attribute_string_value.split(" ")
                    values = [float(value) for value in values]
                    if all([value.is_integer() for value in values]):
                        values = [int(value) for value in values]
                    item_custom[attribute] = values

        items_custom[item_name] = item_custom

    return items_custom


def get_special_conversions():
    return {
            "bonus_strength": "PassiveStrength",
            "bonus_str": "PassiveStrength",
            "bonus_agility": "PassiveAgility",
            "bonus_agi": "PassiveAgility",
            "bonus_int": "PassiveIntelligence",
            "bonus_intellect": "PassiveIntelligence",
            "bonus_intelligence": "PassiveIntelligence",
            "bonus_armor": "PassiveArmor",
            "bonus_damage": "PassiveDamage",
            "bonus_attack_speed": "PassiveAttackSpeed",
            "bonus_magical_armor": "PassiveMagicResistance",
            "bonus_magic_resistance": "PassiveMagicResistance",
            "bonus_spell_resist": "PassiveMagicResistance",
            "magic_resist": "PassiveMagicResistance",
            "magic_resistance": "PassiveMagicResistance",
            "bonus_regen": "PassiveHealthRegen",
            "hp_regen": "PassiveHealthRegen",
            "mana_regen": "PassiveManaRegen",
            "bonus_speed": "PassiveAttackSpeed",
            "movement_speed": "PassiveMovementSpeed",
            "bonus_movement": "PassiveMovementSpeed",
            "bonus_all_stats": "PassiveAllStats",
            "bonus_stats": "PassiveAllStats",
            "lifesteal_percent": "PassiveLifesteal",
            "bonus_health_regen": "PassiveHealthRegen",
            "bonus_health": "PassiveHealth",
            "bonus_evasion": "PassiveEvasion",
            "bonus_mana": "PassiveMana",
            "bonus_spell_amp": "PassiveSpellAmp",
            "spell_amp": "PassiveSpellAmp",
        }


def get_corresponding_attribute(question_type, all_items):
    if question_type == QuestionType.ITEM_COST:
        return "ItemCost"
    elif question_type == QuestionType.ITEM_ACTIVE_COOLDOWN:
        return "AbilityCooldown"
    elif question_type == QuestionType.ITEM_ACTIVE_MANA_COST:
        return "AbilityManaCost"
    elif question_type == QuestionType.ITEM_ACTIVE_RANGE:
        return "AbilityCastRange"
    elif question_type == QuestionType.ITEM_PASSIVE_BONUS:
        return get_random_passive_bonus(all_items)


def get_items_with_attribute(all_items, attribute):
    items_with_attribute = [x for x in all_items.values() if attribute in x]
    skip_zero_value = ["ItemCost", "AbilityCooldown", "AbilityManaCost", "AbilityCastRange"]
    if attribute in skip_zero_value or attribute.startswith("Passive"):
        items_with_attribute = [item for item in items_with_attribute if item[attribute] != [0]]
    return items_with_attribute


def get_random_passive_bonus(all_items):
    all_passive_bonuses = []
    for item_name in all_items:
        item = all_items[item_name]
        for attribute in item:
            if attribute.startswith("Passive") and attribute not in all_passive_bonuses:
                all_passive_bonuses.append(attribute)
    return random.choice(all_passive_bonuses)


def get_random_attribute_from_item_valid_for_question(item):
    exclude_list = ["", "name", "SideShop", "ItemRequirements", "ItemResult"]
    attributes = list(item.keys())
    if all([attribute in exclude_list for attribute in attributes]):
        raise Exception("Invalid ability : no valid attribute " + item["name"])

    attribute = ""
    while attribute in exclude_list:
        attribute = random.choice(attributes)
    return attribute

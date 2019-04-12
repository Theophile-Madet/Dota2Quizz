import vpk
import theo_utils
import json
import random
from question_types import QuestionType


def get_and_save_all_items():
    path = theo_utils.get_dota_folder_base_path() + 'pak01_dir.vpk'
    pak = vpk.open(path)
    items_file = pak.get_file('scripts/npc/items.txt')

    valve_string = items_file.read().decode('utf-8')
    json_string = theo_utils.valve_string_to_json_string(valve_string)

    items_valve = json.loads(json_string)['DOTAAbilities']
    json_string = json.dumps(items_valve, indent=4)
    destination_file = open('items_valve_format.json', 'w+')
    destination_file.write(json_string)
    destination_file.close()

    items_custom = valve_format_to_custom_format(items_valve)
    json_string = json.dumps(items_custom, indent=4)
    destination_file = open('items_custom_format.json', 'w+')
    destination_file.write(json_string)
    destination_file.close()

    return items_custom


def valve_format_to_custom_format(items_valve):
    items_custom = dict()
    name_filter = ["Version", "item_super_blink", "item_pocket_tower", "item_pocket_roshan", "item_mutation_tombstone"]
    attribute_filter = ["EventID", "IsObsolete"]
    kept_attributes = ['AbilityCastRange', 'AbilityCastPoint', 'AbilityCooldown', 'AbilityManaCost', 'ItemCost',
                       'SideShop', 'AbilitySpecial', 'SecretShop', 'ItemInitialCharges', 'IsTempestDoubleClonable',
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

        special_converstions = {
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

        if "AbilitySpecial" in item_valve:
            for special_index in item_valve["AbilitySpecial"]:
                special = item_valve["AbilitySpecial"][special_index]
                for key in special.keys():
                    if key in special_converstions:
                        item_valve[special_converstions[key]] = special[key]

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

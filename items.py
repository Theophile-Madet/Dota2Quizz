import vpk
import theo_utils
import json
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
    name_filter = ["Version"]
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
        for attribute in item_valve:
            if attribute in kept_attributes:
                item_custom[attribute] = [item_valve[attribute]]
                if attribute in convert_to_number_attribute:
                    attribute_string_value = item_valve[attribute]
                    values = attribute_string_value.split(" ")
                    values = [float(value) for value in values]
                    if all([value.is_integer() for value in values]):
                        values = [int(value) for value in values]
                    item_custom[attribute] = values

        items_custom[item_name] = item_custom
    return items_custom


def get_corresponding_attribute(question_type):
    if question_type == QuestionType.ITEM_COST:
        return "ItemCost"


def get_items_with_attribute(all_items, attribute):
    items_with_attribute = [x for x in all_items.values() if attribute in x]
    skip_zero_value = ["ItemCost"]
    if attribute in skip_zero_value:
        items_with_attribute = [item for item in items_with_attribute if item[attribute] != [0]]
    return items_with_attribute

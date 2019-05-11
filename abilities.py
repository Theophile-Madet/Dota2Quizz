import json
import random
import theo_utils
import os.path
import file_paths


def get_abilities_with_attribute(all_abilities, attribute):
    abilities_with_attribute = [x for x in all_abilities.values() if attribute in x]
    skip_zero_value = ["AbilityDamage", "AbilityManaCost", "AbilityCooldown", "AbilityCastRange", "AbilityCastPoint"]
    if attribute in skip_zero_value:
        abilities_with_attribute = [ability for ability in abilities_with_attribute if ability[attribute] != [0]]
    cooldown_exceptions = ["kunkka_return", "naga_siren_song_of_the_siren_cancel", "wisp_tether_break",
                           "monkey_king_untransform", "shadow_demon_shadow_poison_release",
                           "ancient_apparition_ice_blast_release", "techies_focused_detonate"]
    if attribute == "AbilityCooldown":
        abilities_with_attribute = [ability for ability in abilities_with_attribute if
                                    ability["name"] not in cooldown_exceptions]
    return abilities_with_attribute


def get_and_save_all_abilities(ability_name_list):
    create_abilities_custom_file_if_necessary(ability_name_list)
    return theo_utils.load_json_in_file(file_paths.abilities_custom_format())


def create_abilities_custom_file_if_necessary(ability_name_list):
    if not os.path.isfile(file_paths.abilities_custom_format()):
        create_custom_abilities_file(ability_name_list)
        return

    valve_file_path = file_paths.abilities_source_file()
    valve_file_modification_date = os.path.getmtime(valve_file_path)
    custom_file_modification_date = os.path.getmtime(file_paths.abilities_custom_format())
    if valve_file_modification_date > custom_file_modification_date:
        create_custom_abilities_file(ability_name_list)


def create_custom_abilities_file(ability_name_list):
    json_string = get_abilities_json()
    try:
        valve_abilities = json.loads(json_string)["DOTAAbilities"]
    except ValueError as e:
        print('invalid json: %s' % e)
        return None

    json_string = json.dumps(valve_abilities, indent=4)
    destination_file = open(file_paths.abilities_valve_format(), 'w+')
    destination_file.write(json_string)
    destination_file.close()

    custom_abilities = valve_to_custom_format(valve_abilities, ability_name_list)
    custom_abilities = get_valid_abilities(custom_abilities)
    compress_constant_attributes(custom_abilities)

    destination_file = open(file_paths.abilities_custom_format(), 'w+')
    destination_file.write(json.dumps(custom_abilities, indent=4, sort_keys=True))
    destination_file.close()


def valve_to_custom_format(valve_abilities, ability_name_list):
    kept_attributes = ["AbilityDamage", "AbilityManaCost", "AbilityCooldown", "AbilityCastPoint", "AbilityCastRange",
                       "AbilityType"]
    special_conversions = theo_utils.load_json_in_file(file_paths.abilities_special_conversions())

    custom_abilities = dict()
    for ability_name in valve_abilities:
        if ability_name not in ability_name_list:
            continue
        valve_ability = valve_abilities[ability_name]
        custom_ability = dict()
        custom_ability["name"] = ability_name
        for attribute in valve_ability:
            if attribute in kept_attributes:
                custom_ability[attribute] = valve_ability[attribute]

        if ability_name in special_conversions:
            for special_index in valve_ability["AbilitySpecial"]:
                special = valve_ability["AbilitySpecial"][special_index]
                for conversion in special_conversions[ability_name]:
                    for key in special.keys():
                        if key == conversion[0]:
                            custom_ability[conversion[1]] = special[key]
        elif "AbilitySpecial" in valve_ability.keys():
            for special_index in valve_ability["AbilitySpecial"]:
                special = valve_ability["AbilitySpecial"][special_index]
                for original_attribute in special.keys():
                    if original_attribute == "var_type":
                        continue
        #             converted_attribute = input(ability_name + " - " + original_attribute + ": ")
        #             if converted_attribute != '':
        #                 if ability_name not in special_conversions.keys():
        #                     special_conversions[ability_name] = []
        #                 special_conversions[ability_name].append([original_attribute, converted_attribute])
        #
        # json_string = json.dumps(special_conversions, indent=4)
        # destination_file = open('abilities_special_conversions.json', 'w+')
        # destination_file.write(json_string)
        # destination_file.close()

        custom_abilities[ability_name] = custom_ability

    # convert attribute values from string to int list
    for ability in custom_abilities.values():
        for attribute_name in ability:
            if attribute_name == "name" or attribute_name == "AbilityType" or attribute_name == "Abilities":
                continue
            attribute_string_value = ability[attribute_name]
            if not isinstance(attribute_string_value, str):
                continue
            values = attribute_string_value.split(" ")

            values = [float(value) for value in values]
            if all([value.is_integer() for value in values]):
                values = [int(value) for value in values]

            is_constant = all([value == values[0] for value in values])
            if is_constant:
                ability[attribute_name] = [values[0]]
            else:
                ability[attribute_name] = values

    return custom_abilities


def get_abilities_json():
    return theo_utils.load_json_in_file(file_paths.abilities_source_file())


def get_valid_abilities(all_abilities):
    exclude_list = ["Version", "ability_base", "dota_base_ability", "default_attack", "attribute_bonus",
                    "ability_deward", "generic_hidden", "consumable_hidden", "throw_snowball",
                    "elder_titan_echo_stomp_spirit", "keeper_of_the_light_spirit_form", "keeper_of_the_light_recall",
                    "shoot_firework", "techies_focused_detonate", "rubick_telekinesis_land"]
    exclude_substring = ["seasonal", "frostivus", "cny", "greevil", "courier", "roshan", "kobold", "centaur_khan",
                         "spawnlord", "special_bonus", "empty"]
    abilities_filtered = dict()

    for ability_name in all_abilities:
        if ability_name in exclude_list:
            continue
        excluded = False
        for substring in exclude_substring:
            if substring in ability_name:
                excluded = True
                break
        if excluded:
            continue
        abilities_filtered[ability_name] = all_abilities[ability_name]

    return abilities_filtered


def compress_constant_attributes(abilities):
    for ability_name in abilities:
        ability = abilities[ability_name]
        for attribute_name in ability:
            attribute = ability[attribute_name]
            if not isinstance(attribute, str):
                continue
            values = attribute.split(" ")
            is_constant = all([value == values[0] for value in values])
            if is_constant:
                ability[attribute_name] = values[0]


def is_ability_ultimate(ability):
    return "AbilityType" in ability.keys() and ability["AbilityType"] == "DOTA_ABILITY_TYPE_ULTIMATE"


def get_random_attribute_from_ability_valid_for_question(ability):
    exclude_list = ["", "name", "AbilityType"]
    attributes = list(ability.keys())
    if all([attribute in exclude_list for attribute in attributes]):
        raise Exception("Invalid ability : no valid attribute " + ability["name"])

    attribute = ""
    while attribute in exclude_list:
        attribute = random.choice(attributes)
    return attribute


def progress_special_conversions(ability_name_list):
    valve_abilities = theo_utils.load_json_in_file(file_paths.abilities_valve_format())
    special_conversions = theo_utils.load_json_in_file(file_paths.abilities_special_conversions())

    for ability_name in valve_abilities:
        if ability_name not in ability_name_list:
            continue
        valve_ability = valve_abilities[ability_name]

        if ability_name in special_conversions:
            continue
        elif "AbilitySpecial" in valve_ability.keys():
            for special_index in valve_ability["AbilitySpecial"]:
                special = valve_ability["AbilitySpecial"][special_index]
                for original_attribute in special.keys():
                    if original_attribute == "var_type":
                        continue
                    converted_attribute = input(ability_name + " - " + original_attribute + ": ")
                    if converted_attribute != '':
                        if ability_name not in special_conversions.keys():
                            special_conversions[ability_name] = []
                        special_conversions[ability_name].append([original_attribute, converted_attribute])
            break

        json_string = json.dumps(special_conversions, indent=4)
        destination_file = open('abilities_special_conversions.json', 'w+')
        destination_file.write(json_string)
        destination_file.close()


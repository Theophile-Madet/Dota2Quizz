import json
import theo_utils


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


def get_and_save_all_abilities():
    json_string = get_abilities_json()
    try:
        all_abilities = json.loads(json_string)["DOTAAbilities"]
    except ValueError as e:
        print('invalid json: %s' % e)
        return None

    json_string = json.dumps(all_abilities, indent=4)
    destination_file = open('abilities_valve_format.json', 'w+')
    destination_file.write(json_string)
    destination_file.close()

    return all_abilities


def valve_to_custom_format(valve_abilities):
    kept_attributes = ["AbilityDamage", "AbilityManaCost", "AbilityCooldown", "AbilityCastPoint", "AbilityCastRange",
                       "AbilityType"]
    custom_abilities = dict()
    for ability_name in valve_abilities:
        if ability_name == "Version":
            continue
        valve_ability = valve_abilities[ability_name]
        custom_ability = dict()
        custom_ability["name"] = ability_name
        for attribute in valve_ability:
            if attribute in kept_attributes:
                custom_ability[attribute] = valve_ability[attribute]
        custom_abilities[ability_name] = custom_ability

    # convert attribute values from string to int list
    for ability in custom_abilities.values():
        for attribute_name in ability:
            if attribute_name == "name" or attribute_name == "AbilityType":
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
    source_file = open(theo_utils.get_dota_folder_path() + 'npc_abilities.txt',
                       'r')
    valve_string = source_file.read()
    source_file.close()
    return theo_utils.valve_string_to_json_string(valve_string)


def get_valid_abilities(all_abilities):
    exclude_list = ["Version", "ability_base", "dota_base_ability", "default_attack", "attribute_bonus",
                    "ability_deward", "generic_hidden", "consumable_hidden", "throw_snowball",
                    "elder_titan_echo_stomp_spirit", "keeper_of_the_light_spirit_form", "keeper_of_the_light_recall"]
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

import json
import theo_utils


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
            heroes_custom[hero_name] = hero_custom
        except Exception as error:
            print("ERROR BY " + hero_name + "\n\t" + str(error))

    return heroes_custom

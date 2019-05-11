def dota_base_folder():
    return "D:\\SteamLibrary\\steamapps\\common\\dota 2 beta\\game\\dota\\"


def custom_files_folder():
    return ".\\GeneratedFiles\\"


def abilities_source_file():
    return dota_base_folder() + 'scripts\\npc\\npc_abilities.txt'


def abilities_valve_format():
    return custom_files_folder() + "abilities_valve_format.json"


def abilities_custom_format():
    return custom_files_folder() + "abilities_custom_format.json"


def abilities_special_conversions():
    return ".\\abilities_special_conversions.json"


def heroes_source_file():
    return dota_base_folder() + 'scripts\\npc\\npc_heroes.txt'


def heroes_valve_format():
    return custom_files_folder() + "heroes_valve_format.json"


def heroes_custom_format():
    return custom_files_folder() + "heroes_custom_format.json"


def items_source_file_inside_vpk():
    return "scripts/npc/items.txt"


def items_valve_format():
    return custom_files_folder() + "items_valve_format.json"


def items_custom_format():
    return custom_files_folder() + "items_custom_format.json"


def vpk_source_file():
    return dota_base_folder() + 'pak01_dir.vpk'
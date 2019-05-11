import random
import re
import json


def get_dota_constants():
    constants = dict()

    constants["hp_per_str"] = 20
    constants['mana_per_int'] = 12
    constants["armor_per_agi"] = 0.16
    constants["hp_regen_per_str"] = 0.1
    constants["mana_regen_per_int"] = 0.05
    constants["magic_res_per_str"] = 0.0008

    return constants


def randint_rounded(a, b):
    return random.randint(round(a), round(b))


def randfloat(a, b):
    return round(random.uniform(a, b), 2)


def load_json_in_file(path):
    file = open(path, 'r')
    json_string = file.read()
    file.close()
    return json.loads(json_string)


def valve_string_to_json_string(valve_string):
    json_string = '{' + valve_string + '}'

    pattern = r'"([^"]*)"(\s*){'
    replace = r'"\1": {'
    json_string = re.sub(pattern, replace, json_string)

    pattern = r'"([^"]*)"\s*"([^"]*)"'
    replace = r'"\1": "\2",'
    json_string = re.sub(pattern, replace, json_string)

    pattern = r',(\s*[}\]])'
    replace = r'\1'
    json_string = re.sub(pattern, replace, json_string)

    pattern = r'([}\]])(\s*)("[^"]*":\s*)?([{\[])'
    replace = r'\1,\2\3\4'
    json_string = re.sub(pattern, replace, json_string)

    pattern = r'}(\s*"[^"]*":)'
    replace = r'},\1'
    json_string = re.sub(pattern, replace, json_string)

    pattern = r'\/\/[^\n]*\n'
    replace = r''
    json_string = re.sub(pattern, replace, json_string)

    pattern = r'}([^",}]*)"'
    replace = r'},\1"'
    json_string = re.sub(pattern, replace, json_string)

    pattern = r',(\s*[}\]])'
    replace = r'\1'
    json_string = re.sub(pattern, replace, json_string)

    pattern = r'"([^"]*)"(\s*){'
    replace = r'"\1": {'
    json_string = re.sub(pattern, replace, json_string)

    pattern = r'\t'
    replace = r''
    json_string = re.sub(pattern, replace, json_string)

    return json_string

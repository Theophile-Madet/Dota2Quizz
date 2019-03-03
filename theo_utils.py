import random
import re


def randint_rounded(a, b):
    return random.randint(round(a), round(b))


def randfloat(a, b):
    return round(random.uniform(a, b), 2)


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

    return json_string

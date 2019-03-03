import json
import random
import time
import abilities
import heroes
import theo_utils
from question_types import QuestionType


def main():
    print('Welcome to Théo\'s Dota 2 Quizz!\n\n')

    heroes_list = heroes.get_and_save_all_heroes()
    valve_abilities = abilities.get_and_save_all_abilities()
    all_abilities = abilities.valve_to_custom_format(valve_abilities)
    valid_abilities = abilities.get_valid_abilities(all_abilities)
    abilities.compress_constant_attributes(valid_abilities)

    destination_file = open('abilities_custom_format.json', 'w+')
    destination_file.write(json.dumps(valid_abilities, indent=4, sort_keys=True))

    test_all_questions(valid_abilities)
    # ask_random_questions(valid_abilities)


def ask_random_questions(valid_abilities):
    while True:
        question_type = random.choice(list(QuestionType.__members__.values()))
        attribute = get_corresponding_attribute(question_type)
        possible_abilities = abilities.get_abilities_with_attribute(valid_abilities, attribute)
        ability_answer = random.choice(possible_abilities)
        wrong_answers = generate_wrong_answers(possible_abilities, attribute, ability_answer)

        all_answers = wrong_answers.copy()
        correct_index = random.randint(0, 3)
        all_answers.insert(correct_index, ability_answer[attribute])

        print("Question about : " + attribute)
        print("ability is : " + ability_answer["name"])
        for index, answer in enumerate(all_answers):
            print("\t" + str(index + 1) + ") " + " ".join([str(value) for value in answer]))

        user_answer = -1
        while user_answer != correct_index:
            user_answer = int(input("Your answer : ")) - 1
            if user_answer != correct_index:
                print("Wrong!")
        print("\n\nCorrect! " + attribute + " for " + ability_answer["name"] + " is " +
              " ".join([str(round(value, 2)) for value in ability_answer[attribute]]) + "\n\n")
        time.sleep(1)


def test_all_questions(valid_abilities):
    invalid_combinations = []
    question_types = list(QuestionType.__members__.values())
    for question_type in question_types:
        valid_question_count = 0
        attribute = get_corresponding_attribute(question_type)
        possible_abilities = abilities.get_abilities_with_attribute(valid_abilities, attribute)
        debug_abilities = []
        for ability_answer in possible_abilities:
            try:
                generate_wrong_answers(possible_abilities, attribute, ability_answer)
                valid_question_count += 1
                debug_abilities.append(ability_answer["name"])
            except Exception as error:
                print(error)
                combination = dict()
                combination["AbilityName"] = ability_answer["name"]
                combination["AttributeName"] = attribute
                combination["AttributeValue"] = ability_answer[attribute]
                invalid_combinations.append(combination)
        print(str(question_type) + " has " + str(valid_question_count) + " valid questions")
        # print(debug_abilities)
    print(invalid_combinations)


def generate_wrong_answers(possible_abilities, attribute, ability_answer):
    wrong_answers = []
    tries = 0
    while len(wrong_answers) < 3:
        potential_answer = generate_wrong_answer(possible_abilities, attribute, ability_answer)
        if potential_answer in wrong_answers or ability_answer[attribute] == potential_answer:
            tries += 1
            if tries > 100:
                raise Exception(
                    "Can't generate answers for " + ability_answer["name"] + " " + attribute + " " + " ".join(
                        [str(value) for value in ability_answer[attribute]]))
            continue
        wrong_answers.append(potential_answer)
    return wrong_answers


def generate_wrong_answer(possible_abilities, attribute, ability_answer):
    value_source = random.choice(["generated"])
    # value_sources = random.choice(["from_other_ability", "generated"])
    # value_count = random.choice(["same", "different"])

    value = None
    if value_source == "generated":
        value = generate_similar_answer(ability_answer[attribute],
                                        attribute_allows_negative_upgrade(attribute),
                                        abilities.is_ability_ultimate(ability_answer))
    return value


def generate_similar_answer(correct_answer, allow_negative_upgrade, is_ultimate):
    # print("Generating from : " + correct_answer + " " + str(allow_negative_upgrade))

    all_values_multiple_of_5 = all([x % 5 == 0 and x >= 20 for x in correct_answer])
    # print("all_values_multiple_of_5 : " + str(all_values_multiple_of_5))
    if random.random() < 0.1:
        all_values_multiple_of_5 = not all_values_multiple_of_5
        # print("Flip multiple of 5")

    all_values_integer = all([isinstance(value, int) or value.is_integer() and value > 1 for value in correct_answer])
    if random.random() < 0.1:
        all_values_integer = not all_values_integer
    if all_values_integer:
        random_function = theo_utils.randint_rounded
    else:
        random_function = theo_utils.randfloat

    generated_start_value = random_function(correct_answer[0] * 0.75, correct_answer[0] * 1.25)

    if all_values_multiple_of_5 and generated_start_value % 5 != 0:
        generated_start_value = round(generated_start_value / 5) * 5
    generated_answer = [generated_start_value]

    has_multiple_values = len(correct_answer) > 1
    # print("has_multiple_values : " + str(has_multiple_values))
    if random.random() < 0.1:
        # print("Flip multiple values")
        has_multiple_values = not has_multiple_values

    target_value_count = len(correct_answer)
    if has_multiple_values and len(correct_answer) == 1:
        if is_ultimate:
            target_value_count = 3
        else:
            target_value_count = 4

    if has_multiple_values:
        if has_multiple_values and len(correct_answer) == 1:
            average_upgrade = random_function(-correct_answer[0] * 0.5, correct_answer[0] * 0.5)
            all_upgrade_equal = random.random() > 0.2
        else:
            upgrades = [correct_answer[i + 1] - correct_answer[i] for i in range(len(correct_answer) - 1)]
            average_upgrade = sum(upgrades) / len(upgrades)
            all_upgrade_equal = all([upgrade == average_upgrade for upgrade in upgrades])
            if random.random() < 0.1:
                all_upgrade_equal = not all_upgrade_equal

        if all_upgrade_equal:
            lower_bound = round(average_upgrade * 0.75)
            if not allow_negative_upgrade:
                lower_bound = round(average_upgrade)
            bounds = [lower_bound, round(average_upgrade * 1.25)]
            generated_upgrade = random_function(min(bounds), max(bounds))

            if all_values_multiple_of_5:
                generated_upgrade = round(generated_upgrade / 5) * 5

            while len(generated_answer) < target_value_count:
                generated_answer.append(generated_answer[-1] + generated_upgrade)
        else:
            if not allow_negative_upgrade:
                upgrade_is_positive = True
            else:
                upgrade_is_positive = average_upgrade > 0
                if random.random() < 0.1:
                    upgrade_is_positive = not upgrade_is_positive

            while len(generated_answer) < target_value_count:
                bounds = [round(average_upgrade * 0.75), round(average_upgrade * 1.25)]
                generated_upgrade = abs(random_function(min(bounds), max(bounds)))
                if not upgrade_is_positive:
                    generated_upgrade *= -1
                if all_values_multiple_of_5:
                    generated_upgrade = round(generated_upgrade / 5) * 5
                generated_answer.append(generated_answer[-1] + generated_upgrade)

    return generated_answer


def get_corresponding_attribute(question_type):
    if question_type == QuestionType.ABILITY_DAMAGE:
        return "AbilityDamage"
    if question_type == QuestionType.ABILITY_MANA_COST:
        return "AbilityManaCost"
    if question_type == QuestionType.ABILITY_COOLDOWN:
        return "AbilityCooldown"
    if question_type == QuestionType.ABILITY_CAST_POINT:
        return "AbilityCastPoint"
    if question_type == QuestionType.ABILITY_RANGE:
        return "AbilityCastRange"


def get_valid_attributes(abilities):
    valid_attributes = []

    exclude_list = ["ID", "AbilitySound", "HasScepterUpgrade", "FightRecapLevel", "MaxLevel", "IsGrantedByScepter",
                    "AbilityDraftPreAbility", "HotKeyOverride", "DisplayAdditionalHeroes", "AbilityTextureName",
                    "precache", "Modelscale", "AbilitySharedCooldown", "AbilityChannelAnimation",
                    "AbilityUnitTargetTeam", "AbilityCastAnimation", "AbilityType", "RequiredLevel",
                    "AbilityCastGestureSlot", "AbilitySpecial", "OnCastbar", "LinkedAbility", "OnLearnbar",
                    "AbilityBehavior"]
    exclude_substring = []

    for ability_name in abilities:
        for attribute_name in abilities[ability_name]:
            if attribute_name in valid_attributes:
                continue
            if attribute_name in exclude_list:
                continue
            excluded = False
            for substring in exclude_substring:
                if substring in ability_name:
                    excluded = True
                    break
            if excluded:
                continue
            valid_attributes.append(attribute_name)

    return valid_attributes


def attribute_allows_negative_upgrade(attribute):
    forbid_list = ["AbilityDamage"]
    if attribute in forbid_list:
        return False
    else:
        return True


if __name__ == '__main__':
    main()
